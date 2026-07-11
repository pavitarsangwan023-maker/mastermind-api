import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\server.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Add Secret Notes API Routes
secret_routes = r"""
// ============================================================
// SECRET BOX API ROUTES
// ============================================================
const SecretNote = require('./models/SecretNote');

app.post('/api/secrets', async (req, res) => {
  const { email, content } = req.body;
  if (!email || !content) return res.status(400).json({ success: false, error: 'Missing data' });
  
  try {
    const newNote = new SecretNote({ userEmail: email, content });
    await newNote.save();
    res.json({ success: true, message: 'Secret saved.' });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

app.get('/api/secrets', async (req, res) => {
  const { email } = req.query;
  if (!email) return res.status(400).json({ success: false, error: 'Missing email' });
  
  try {
    const notes = await SecretNote.find({ userEmail: email }).sort({ createdAt: -1 });
    res.json({ success: true, secrets: notes });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});
"""

code = re.sub(
    r"// ============================================================\n// USER PUSH TOKEN ROUTE\n// ============================================================",
    secret_routes.strip() + "\n\n// ============================================================\n// USER PUSH TOKEN ROUTE\n// ============================================================",
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated server.js to support Secret Box.")
