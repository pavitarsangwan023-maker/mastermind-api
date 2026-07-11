import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\server.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

new_routes = r"""
// ============================================================
// USER PUSH TOKEN ROUTE
// ============================================================
const User = require('./models/User');
const Reminder = require('./models/Reminder');

app.post('/api/user/token', async (req, res) => {
  const { email, expoPushToken } = req.body;
  if (!email || !expoPushToken) return res.status(400).json({ success: false, error: 'Missing data' });
  
  try {
    let user = await User.findOne({ email });
    if (!user) {
      user = new User({ email, expoPushToken });
    } else {
      user.expoPushToken = expoPushToken;
    }
    await user.save();
    res.json({ success: true, message: 'Push token registered successfully' });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});
"""

code = re.sub(
    r"// ============================================================\n// QUOTA API ROUTE\n// ============================================================",
    new_routes.strip() + "\n\n// ============================================================\n// QUOTA API ROUTE\n// ============================================================",
    code
)

reminder_logic = r"""
    // 2. FAST REMINDERS
    const reminderRegex = /(remind me|reminder|yaad dila|याद दिला|रिमाइंडर)[\s\S]*?(\d+)\s*(sec|second|min|minute|hr|hour|day|सेकंड|मिनट|घंट|दिन)/i;
    const reminderRegexRev = /(\d+)\s*(sec|second|min|minute|hr|hour|day|सेकंड|मिनट|घंट|दिन)[\s\S]*?(remind|yaad dila|याद दिला|रिमाइंडर)/i;
    
    const reminderMatch = lowerText.match(reminderRegex) || lowerText.match(reminderRegexRev);
    if (reminderMatch) {
       let num = parseInt(reminderMatch[2] || reminderMatch[1]);
       let unit = (reminderMatch[3] || reminderMatch[2]).toLowerCase();
       let delayMs = 0;
       if (unit.startsWith('sec') || unit.startsWith('सेक')) delayMs = num * 1000;
       else if (unit.startsWith('min') || unit.startsWith('मिन')) delayMs = num * 60 * 1000;
       else if (unit.startsWith('hr') || unit.startsWith('hour') || unit.startsWith('घंट')) delayMs = num * 60 * 60 * 1000;
       else if (unit.startsWith('day') || unit.startsWith('दिन')) delayMs = num * 24 * 60 * 60 * 1000;
       
       if (delayMs > 0) {
           let safeUnit = unit.startsWith('सेक') ? 'second' : (unit.startsWith('मिन') ? 'minute' : (unit.startsWith('घंट') ? 'hour' : (unit.startsWith('दिन') ? 'day' : unit)));
           
           // Database Save (if email is provided by frontend)
           const userEmail = req.body.email; // Frontend needs to send this
           if (userEmail) {
              try {
                  const dueDate = new Date(Date.now() + delayMs);
                  const newReminder = new Reminder({
                      userEmail: userEmail,
                      taskText: text,
                      dueDate: dueDate
                  });
                  await newReminder.save();
                  console.log(`[DB] Saved reminder for ${userEmail} due at ${dueDate}`);
              } catch(e) {
                  console.error('[DB Error] Failed to save reminder:', e);
              }
           }

           return res.json({
               success: true,
               aiResponse: `Thik hai ${userTitle}, main aapko ${num} ${safeUnit} baad yaad dila dungi.`,
               action: "REMINDER",
               reminderDelayMs: delayMs
           });
       }
    }
"""

code = code.replace(
    code[code.find("// 2. FAST REMINDERS"):code.find("// 3. FAST MUSIC")],
    reminder_logic.strip() + "\n\n    "
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated server.js to support Push Token and DB Reminders.")
