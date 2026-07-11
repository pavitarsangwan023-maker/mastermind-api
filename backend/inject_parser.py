import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\server.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

local_router = """
    // ============================================================
    // LOCAL INTENT ROUTER (BYPASS GEMINI FOR SIMPLE TASKS)
    // ============================================================
    const lowerText = text.toLowerCase();
    
    // 1. FAST STOP
    if (lowerText.match(/^(stop|chup|band kar|ruko|hatao)$/)) {
       return res.json({ success: true, aiResponse: "Thik hai, band kar diya.", action: "STOP_MUSIC" });
    }

    // 2. FAST REMINDERS
    const reminderMatch = lowerText.match(/(remind me|reminder|yaad dila).*?(\\d+)\\s*(sec|second|min|minute|hr|hour)/) || lowerText.match(/(\\d+)\\s*(sec|second|min|minute|hr|hour).*?(remind|yaad dila)/);
    if (reminderMatch) {
       let num = parseInt(reminderMatch[2] || reminderMatch[1]);
       let unit = (reminderMatch[3] || reminderMatch[2]);
       let delayMs = 0;
       if (unit.startsWith('sec')) delayMs = num * 1000;
       else if (unit.startsWith('min')) delayMs = num * 60 * 1000;
       else if (unit.startsWith('hr') || unit.startsWith('hour')) delayMs = num * 60 * 60 * 1000;
       
       if (delayMs > 0) {
           return res.json({
               success: true,
               aiResponse: `Thik hai ${userTitle}, main aapko ${num} ${unit} baad yaad dila dungi.`,
               action: "REMINDER",
               reminderDelayMs: delayMs
           });
       }
    }

    // 3. FAST MUSIC
    const musicMatch = lowerText.match(/(play|gaana chalao|song|music)\\s*(.*?)$/) || lowerText.match(/^(.*?)\\s*(play|gaana chalao|song|music)$/);
    if (musicMatch && (lowerText.includes('play') || lowerText.includes('gaana') || lowerText.includes('song'))) {
       // Filter out common verbs to get query
       let query = lowerText.replace(/play|gaana chalao|gaana sunna|song|music|sunao|chalao/g, '').trim();
       if (!query) query = "latest hindi songs";
       return res.json({
           success: true,
           aiResponse: `Thik hai, main aapke liye ${query} chala rahi hu.`,
           action: "PLAY_MUSIC",
           searchQuery: query
       });
    }
    // ============================================================
"""

# Insert right after `const { text, apiKey, userTitle } = req.body;` validations.
target_line = "console.log(`[DEBUG] Using key: \"${apiKey.trim().substring(0, 10)}...\" | Text: \"${text.substring(0, 30)}\"`);"
code = code.replace(target_line, target_line + "\n" + local_router)

# Remove the old `const lowerText = text.toLowerCase();` that was further down
# We just need to make sure we don't declare it twice.
code = code.replace("const lowerText = text.toLowerCase();\n    if (lowerText.includes('weather')", "if (lowerText.includes('weather')")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Local Intent Router injected!")
