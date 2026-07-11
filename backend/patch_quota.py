import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\server.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Fix the backend quota limit from 1500 to 10000
code = re.sub(
    r"res\.json\(\{ usage: globalQuota\.count, limit: 1500 \}\);",
    "res.json({ usage: globalQuota.count, limit: 10000 });",
    code
)
code = re.sub(
    r"const remaining = 1500 - apiUsageToday;",
    "const remaining = 10000 - apiUsageToday;",
    code
)
code = re.sub(
    r"out of their 1500 free limit\.",
    "out of their 10000 limit.",
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated server.js quota to 10000.")
