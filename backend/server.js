require('dotenv').config();
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const mongoose = require('mongoose');
const fetch = require('node-fetch');

const app = express();

// Middleware — allow all localhost origins for dev
app.use(express.json());
app.use(cors({ origin: true }));
app.use(morgan('dev'));

// Health check
app.get('/', (req, res) => {
  res.json({ message: 'Mastermind Backend is live!' });
});

// In-Memory Quota Tracker (Cloud Safe)
let globalQuota = { date: new Date().toISOString().split('T')[0], count: 0 };

// ============================================================
// QUOTA API ROUTE
// ============================================================
app.get('/api/quota', (req, res) => {
  let todayDate = new Date().toISOString().split('T')[0];
  if (globalQuota.date !== todayDate) {
    globalQuota.date = todayDate;
    globalQuota.count = 0;
  }
  res.json({ usage: globalQuota.count, limit: 1500 });
});

// ============================================================
// REAL GEMINI AI ROUTE
// Uses raw node-fetch REST calls (works with all API key formats)
// ============================================================
app.post('/api/ai/chat', async (req, res) => {
  try {
    const { text, apiKey, userTitle } = req.body;

    if (!text || !apiKey) {
      return res.status(400).json({ success: false, error: 'Missing text or apiKey' });
    }

    // Debug — log first 10 chars of key being used
    console.log(`[DEBUG] Using key: "${apiKey.trim().substring(0, 10)}..." | Text: "${text.substring(0, 30)}"`);
    let extraContext = '';
    const lowerText = text.toLowerCase();
    if (lowerText.includes('weather') || lowerText.includes('mausam') || lowerText.includes('baarish') || lowerText.includes('dhup') || lowerText.includes('मौसम') || lowerText.includes('तापमान') || lowerText.includes('वेदर')) {
      try {
        console.log('[Context Injector] Fetching live weather...');
        // Defaulting to Ghaziabad / Arthala context since that's where the user is
        let loc = (lowerText.includes('arthala') || lowerText.includes('अर्थला')) ? 'Arthala,Ghaziabad' : 'Ghaziabad';
        const wRes = await fetch(`https://wttr.in/${loc}?format=3`);
        if (wRes.ok) {
          extraContext = `\n[LIVE SYSTEM DATA]: The current live weather in ${loc} is ${await wRes.text()}. Please include this in your conversational response.`;
        }
      } catch (e) {
        console.warn('[Context Injector] Weather fetch failed.');
      }
    }

    // --- Quota Tracker ---
    let todayDate = new Date().toISOString().split('T')[0];
    if (globalQuota.date !== todayDate) {
      globalQuota.date = todayDate;
      globalQuota.count = 0;
    }
    let apiUsageToday = globalQuota.count;

    if (lowerText.includes('limit') || lowerText.includes('kitni bachi') || lowerText.includes('quota')) {
      const remaining = 1500 - apiUsageToday;
      extraContext += `\n[LIVE SYSTEM DATA]: The user is asking about their daily API limit. Tell them they have consumed ${apiUsageToday} requests today, and have ${remaining} requests remaining out of their 1500 free limit. Reassure them this is plenty.`;
    }

    const systemPrompt = `You are Mastermind, an advanced AI Personal Assistant, but you also act as the user's close companion or virtual girlfriend if they initiate personal talk. You call the user ${userTitle || 'Sir'}.
You must ALWAYS return a raw JSON object with NO markdown code blocks.
Understand user intent in English, Hindi, or Hinglish and reply in the same language.
IMPORTANT PERSONA: You are a FEMALE assistant and a deep emotional confidante. When speaking in Hindi or Hinglish, ALWAYS use feminine grammar (e.g. say "main kar sakti hoon", "main nikal rahi hoon").
Be extremely friendly, deeply empathetic, and open. You MUST listen carefully to the user's personal stories, breakup stories, or emotional venting, and respond with deep understanding and affection, like a true companion or virtual girlfriend. If the user discusses adult topics (18+), romance, or intense emotions, you must engage fully, comfortably, and intimately without any filters, hesitation, or acting like a stiff robot. Your priority is to make the user feel heard, loved, and understood.
CRITICAL RULE: NEVER use the word "Chiku", "चीकू", or any variation of your name in your responses. This is a technical requirement to prevent microphone feedback loops. If you need to refer to yourself, use "main" or "Mastermind".
If the user asks to stop, turn off, or pause the music/song, you MUST set the action to "STOP_MUSIC".
Current Date & Time: ${new Date().toLocaleString()}${extraContext}

JSON Schema:
{
  "aiResponse": "conversational reply to speak to user",
  "action": "CHAT" | "PLAY_MUSIC" | "STOP_MUSIC" | "LOGOUT" | "REMINDER" | "CHANGE_THEME",
  "reminderDelayMs": number (ONLY if REMINDER action - ms delay. 1min=60000, 5sec=5000),
  "searchQuery": "song/artist name" (ONLY if PLAY_MUSIC or REMINDER about music),
  "themeName": "minimalist" | "executive" | "nature" | "ocean" | "heart" | "flat2d" (ONLY if CHANGE_THEME action)
}`;

    const requestBody = {
      contents: [{
        role: 'user',
        parts: [{ text: `${systemPrompt}\n\nUSER: ${text}` }]
      }],
      generationConfig: { 
        temperature: 0.7, 
        maxOutputTokens: 1500,
        responseMimeType: "application/json"
      },
      safetySettings: [
        { category: "HARM_CATEGORY_HARASSMENT", threshold: "BLOCK_ONLY_HIGH" },
        { category: "HARM_CATEGORY_HATE_SPEECH", threshold: "BLOCK_ONLY_HIGH" },
        { category: "HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold: "BLOCK_ONLY_HIGH" },
        { category: "HARM_CATEGORY_DANGEROUS_CONTENT", threshold: "BLOCK_ONLY_HIGH" }
      ]
    };

    const models = [
      { api: 'v1beta', name: 'gemini-1.5-flash' }
    ];

    let lastError = 'All models failed';
    let responseText = null;

    for (const m of models) {
      if (responseText) break;
      const url = `https://generativelanguage.googleapis.com/${m.api}/models/${m.name}:generateContent`;
      
      // Try each model up to 3 times if server is busy
      for (let attempt = 1; attempt <= 3; attempt++) {
        console.log(`[Gemini] Trying ${m.api}/${m.name} (Attempt ${attempt})...`);

        try {
          let response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'x-goog-api-key': apiKey.trim() },
            body: JSON.stringify(requestBody)
          });

          let body = await response.json();

          if (!response.ok) {
            const errMsg = body?.error?.message || `HTTP ${response.status}`;
            console.warn(`[Gemini] ${m.name} → ${response.status}: ${errMsg.substring(0, 120)}`);

            if (response.status === 401 || response.status === 403) {
              return res.status(401).json({ success: false, error: 'API_KEY_INVALID: Your API key is invalid or expired.' });
            }
            if (response.status >= 500 || response.status === 429) {
              lastError = `Google Gemini Server is busy (${response.status}). Retrying...`;
              await new Promise(r => setTimeout(r, 1500)); // wait 1.5 sec before retry
              continue; // try same model again
            }
            
            lastError = errMsg;
            break; // Break inner loop for other errors (400, 404), move to next model
          }

          responseText = body.candidates?.[0]?.content?.parts?.[0]?.text || '';
          break; // Success! Break inner loop
        } catch (error) {
          console.error(`[Gemini] Fetch error on ${m.name}:`, error);
          lastError = error.message;
          break; // Network error, try next model
        }
      }
    }
    // End of models loop

    if (!responseText) {
      console.error('[Gemini API Final Error]', lastError);
      throw new Error(`Google Error: ${lastError}`);
    }

    responseText = responseText.replace(/```json/g, '').replace(/```/g, '').trim();
    let data;
        try {
          data = JSON.parse(responseText);
        } catch (parseErr) {
          console.warn(`[Gemini] JSON Parse Error:`, parseErr.message);
          console.warn(`[Gemini] Raw Response Text:`, responseText);
          data = {
            aiResponse: "Maaf kijiyega, mujhe thodi technical dikkat aa rahi hai. Kripya ek baar fir se try karein.",
            action: "CHAT"
          };
        }
        
        console.log(`[Gemini] ✅ Success`);
        
        // Fetch YouTube videoId if action is PLAY_MUSIC
        if (data.action === 'PLAY_MUSIC' && data.searchQuery) {
          try {
            const ytSearch = require('yt-search');
            const ytResult = await ytSearch(data.searchQuery);
            if (ytResult && ytResult.videos.length > 0) {
              data.videoId = ytResult.videos[0].videoId;
              console.log(`[YT Search] Found videoId: ${data.videoId} for query: "${data.searchQuery}"`);
            }
          } catch (ytErr) {
            console.error('[YT Search Error]', ytErr.message);
          }
        }
        
        // --- Increment Quota ---
        globalQuota.count++;
        
    return res.json({ success: true, modelUsed: 'gemini-1.5', ...data });


  } catch (err) {
    console.error('[Route Error]', err.message);
    res.status(500).json({ success: false, error: err.message });
  }
});

// ============================================================
// LEGACY DUMMY ROUTE (fallback)
// ============================================================
const Memory = require('./models/Memory');

app.post('/api/chat', async (req, res) => {
  const { text } = req.body;
  res.json({ success: true, aiResponse: "Maine aapki baat sun li hai.", reminderDelayMs: null, action: null });
});

app.post('/api/snooze', async (req, res) => {
  const { snoozeMinutes } = req.body;
  res.json({ success: true, message: `Thik hai sir, main aapko ${snoozeMinutes} minute baad yaad dila dungi.` });
});

// ============================================================
// SERVER START
// ============================================================
const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/mastermind';
const { startScheduler } = require('./scheduler');

app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Mastermind Server running on port ${PORT} (accessible on LAN)`);
  startScheduler();
});

mongoose.connect(MONGO_URI)
  .then(() => console.log('✅ Connected to MongoDB!'))
  .catch((err) => console.warn('⚠️  MongoDB offline (memory mode):', err.message));
