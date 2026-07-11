import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\server.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Fix 1: Fallback Array Expansion
# If gemini-1.5-flash gives 429, it should fallback to other models instantly instead of just waiting and retrying the same one.
models_logic = """
    const models = [
      { api: 'v1beta', name: 'gemini-1.5-flash' },
      { api: 'v1beta', name: 'gemini-1.5-pro' },
      { api: 'v1beta', name: 'gemini-pro' }
    ];
"""
code = re.sub(
    r"    const models = \[\n      \{ api: 'v1beta', name: 'gemini-1\.5-flash' \}\n    \];",
    models_logic.strip(),
    code
)

# Fix 2: Better 429 handling. If 429, don't just sleep and continue (which retries same model if attempt <= 2),
# actually break out of the attempt loop so it moves to the NEXT model in the array instantly.
retry_logic = """
            if (response.status >= 500 || response.status === 429) {
              lastError = `Google Error (${response.status}): Servers overloaded. Trying another model...`;
              console.warn(lastError);
              break; // Break attempt loop to move to the NEXT model immediately
            }
"""
code = re.sub(
    r"            if \(response\.status >= 500 \|\| response\.status === 429\) \{.*?continue; \n            \}",
    retry_logic.strip(),
    code,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated server.js for 429 fallback logic.")
