import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\scheduler.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace the title logic
old_title_logic = r"""                    title: 'Mastermind Reminder ⏰',"""
new_title_logic = r"""                    title: reminder.taskText.length > 40 ? reminder.taskText.substring(0, 40) + '...' : reminder.taskText,"""

code = code.replace(old_title_logic, new_title_logic)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated scheduler.js title logic.")
