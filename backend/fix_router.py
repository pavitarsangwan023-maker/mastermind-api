import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\server.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Remove gemini-1.5-flash-8b from models
code = re.sub(
    r"\{\s*api:\s*'v1beta',\s*name:\s*'gemini-1.5-flash-8b'\s*\}",
    "",
    code
)
# Fix array formatting if trailing comma exists
code = code.replace(",\n    ];", "\n    ];").replace("    \n", "")

new_router = """
    // ============================================================
    // LOCAL INTENT ROUTER (BYPASS GEMINI FOR SIMPLE TASKS)
    // ============================================================
    const lowerText = text.toLowerCase();
    
    // 1. FAST STOP
    if (lowerText.match(/^(stop|chup|band kar|ruko|hatao|बंद|चुप|रुक)$/)) {
       return res.json({ success: true, aiResponse: "Thik hai, band kar diya.", action: "STOP_MUSIC" });
    }

    // 2. FAST REMINDERS
    const reminderRegex = /(remind me|reminder|yaad dila|याद दिला|रिमाइंडर).*?(\\d+)\\s*(sec|second|min|minute|hr|hour|सेकंड|मिनट|घंट)/i;
    const reminderRegexRev = /(\\d+)\\s*(sec|second|min|minute|hr|hour|सेकंड|मिनट|घंट).*?(remind|yaad dila|याद दिला|रिमाइंडर)/i;
    
    const reminderMatch = lowerText.match(reminderRegex) || lowerText.match(reminderRegexRev);
    if (reminderMatch) {
       let num = parseInt(reminderMatch[2] || reminderMatch[1]);
       let unit = (reminderMatch[3] || reminderMatch[2]).toLowerCase();
       let delayMs = 0;
       if (unit.startsWith('sec') || unit.startsWith('सेक')) delayMs = num * 1000;
       else if (unit.startsWith('min') || unit.startsWith('मिन')) delayMs = num * 60 * 1000;
       else if (unit.startsWith('hr') || unit.startsWith('hour') || unit.startsWith('घंट')) delayMs = num * 60 * 60 * 1000;
       
       if (delayMs > 0) {
           let safeUnit = unit.startsWith('सेक') ? 'second' : (unit.startsWith('मिन') ? 'minute' : (unit.startsWith('घंट') ? 'hour' : unit));
           return res.json({
               success: true,
               aiResponse: `Thik hai ${userTitle}, main aapko ${num} ${safeUnit} baad yaad dila dungi.`,
               action: "REMINDER",
               reminderDelayMs: delayMs
           });
       }
    }

    // 3. FAST MUSIC
    const musicMatch = lowerText.match(/(play|gaana chalao|song|music|गाना|सुनाओ|चलाओ|बजाओ)\\s*(.*?)$/i) || lowerText.match(/^(.*?)\\s*(play|gaana chalao|song|music|गाना|सुनाओ|चलाओ|बजाओ)/i);
    if (musicMatch && (lowerText.includes('play') || lowerText.includes('gaana') || lowerText.includes('song') || lowerText.includes('गाना'))) {
       // Filter out common verbs to get query
       let query = lowerText.replace(/play|gaana chalao|gaana sunna|song|music|sunao|chalao|बजाओ|सुनाओ|गाना|मुझे/g, '').trim();
       if (!query) query = "latest hindi songs";
       return res.json({
           success: true,
           aiResponse: `Thik hai, main aapke liye ${query} chala rahi hu.`,
           action: "PLAY_MUSIC",
           searchQuery: query
       });
    }

    // 4. FAST TIME
    if (lowerText.match(/^(time kya|kya time|samay kya|time batao|what is the time|current time|समय क्या|क्या टाइम|टाइम बताओ)/i)) {
       const now = new Date();
       let hours = now.getHours();
       let minutes = now.getMinutes();
       hours = hours % 12;
       hours = hours ? hours : 12; 
       const timeStr = `${hours} bajkar ${minutes} minute ho rahe hain.`;
       return res.json({ success: true, aiResponse: `Sir, abhi ${timeStr}`, action: "CHAT" });
    }

    // 5. FAST WEATHER
    if (lowerText.match(/weather|mausam|baarish|dhup|मौसम|तापमान|वेदर/i)) {
      try {
        let loc = (lowerText.includes('arthala') || lowerText.includes('अर्थला')) ? 'Arthala,Ghaziabad' : 'Ghaziabad';
        const wRes = await fetch(`https://wttr.in/${loc}?format=3`);
        if (wRes.ok) {
           const wText = await wRes.text();
           return res.json({ success: true, aiResponse: `Sir, ${loc} ka live weather hai: ${wText.replace('+', '')}.`, action: "CHAT" });
        }
      } catch (e) {
        console.warn('Weather fetch failed.');
      }
    }
    // ============================================================
"""

# Now replace the old router block
# The old router starts at // ============================================================ \n    // LOCAL INTENT ROUTER
# And ends at // ============================================================ \n\n    let extraContext
code = re.sub(
    r"// ============================================================\s*// LOCAL INTENT ROUTER.*?// ============================================================",
    new_router.strip(),
    code,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)
print("Updated router and removed bad models.")
