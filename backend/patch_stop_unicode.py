import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\server.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Fix Stop Regex: \b doesn't work for unicode/hindi characters. We should just use a simple match.
stop_logic = """
// 1. FAST STOP
    if (lowerText.match(/(stop|chup|band kar|ruko|hatao|बंद|चुप|रुक|स्टॉप|रुक जाओ)/i)) {
       return res.json({ success: true, aiResponse: "Thik hai, band kar diya.", action: "STOP_MUSIC" });
    }
"""
code = re.sub(
    r"// 1\. FAST STOP.*?if \(lowerText\.match\(\/\(\?:.*?\}\n",
    stop_logic.strip() + "\n",
    code,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated server.js for Unicode Stop Fix.")
