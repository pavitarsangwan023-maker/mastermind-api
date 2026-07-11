import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\server.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update the FAST STOP logic to be even more aggressive (it already is quite aggressive, but let's ensure it catches "chiku stop")
new_stop_logic = """
    // 1. FAST STOP
    if (lowerText.match(/(stop|chup|band kar|ruko|hatao|बंद|चुप|रुक)/)) {
       return res.json({ success: true, aiResponse: "Thik hai, band kar diya.", action: "STOP_MUSIC" });
    }
"""
code = re.sub(
    r"// 1\. FAST STOP.*?if \(lowerText\.match\(\/\^\(.*?\}\n",
    new_stop_logic.strip() + "\n",
    code,
    flags=re.DOTALL
)

# 2. Add dynamic model discovery inside the Gemini fallback loop
# The loop looks like:
#     let lastError = 'Google Gemini servers are currently overloaded. Please wait a moment and try again.';
#     let responseText = null;
#     for (const m of models) {
dynamic_model_logic = """
    let lastError = 'Google Gemini servers are currently overloaded. Please wait a moment and try again.';
    let responseText = null;

    let dynamicModels = [...models];

    for (let i = 0; i < dynamicModels.length; i++) {
      if (responseText) break;
      const m = dynamicModels[i];
      const url = `https://generativelanguage.googleapis.com/${m.api}/models/${m.name}:generateContent`;
      
      // Try each model up to 2 times
      for (let attempt = 1; attempt <= 2; attempt++) {
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
            
            // DYNAMIC DISCOVERY ON 404 (Model Not Found)
            if (response.status === 404 && errMsg.includes('not found') && i === dynamicModels.length - 1) {
                console.log(`[Gemini] Model 404. Attempting dynamic discovery...`);
                try {
                    const listRes = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey.trim()}`);
                    const listData = await listRes.json();
                    if (listData.models) {
                        const available = listData.models.filter(mdl => mdl.name.includes('gemini') && mdl.supportedGenerationMethods.includes('generateContent'));
                        if (available.length > 0) {
                            const newModelName = available[0].name.replace('models/', '');
                            console.log(`[Gemini] Dynamically found model: ${newModelName}. Retrying...`);
                            dynamicModels.push({ api: 'v1beta', name: newModelName });
                            lastError = `Discovered ${newModelName}`;
                            break; // break inner attempt loop, outer loop will continue with the new model
                        }
                    }
                } catch(e) {
                    console.log('Dynamic discovery failed:', e.message);
                }
            }

            if (response.status >= 500 || response.status === 429) {
              lastError = `Google Error (${response.status}): Servers overloaded.`;
              await new Promise(r => setTimeout(r, 2000));
              continue; 
            }
            
            lastError = `Google Error (${response.status}): ${errMsg}`;
            break; 
          }

          responseText = body.candidates?.[0]?.content?.parts?.[0]?.text || '';
          break; // Success!
        } catch (error) {
           console.error(`[Gemini] Fetch error on ${m.name}:`, error);
          lastError = error.message;
          break; // Network error
        }
      }
    }
    // End of models loop
"""
code = re.sub(
    r"    let lastError = 'Google Gemini.*?// End of models loop\n",
    dynamic_model_logic,
    code,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated server.js with dynamic model fallback and aggressive STOP.")
