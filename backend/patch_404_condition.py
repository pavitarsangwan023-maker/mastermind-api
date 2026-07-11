import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\server.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Fix the dynamic discovery check to include "no longer available"
discovery_logic = """
            // DYNAMIC DISCOVERY ON 404 (Model Not Found or No Longer Available)
            if (response.status === 404 && (errMsg.includes('not found') || errMsg.includes('no longer available')) && i === dynamicModels.length - 1) {
"""
code = re.sub(
    r"            // DYNAMIC DISCOVERY ON 404.*?if \(response\.status === 404 && errMsg\.includes\('not found'\) && i === dynamicModels\.length - 1\) \{",
    discovery_logic.strip(),
    code,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated server.js for dynamic model discovery condition.")
