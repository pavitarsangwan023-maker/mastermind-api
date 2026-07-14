import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\scheduler.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Change setInterval from 60000 (1 minute) to 5000 (5 seconds)
code = code.replace("}, 60000);", "}, 5000);")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated scheduler.js to poll every 5 seconds")
