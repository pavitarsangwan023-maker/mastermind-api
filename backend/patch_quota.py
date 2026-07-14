import re

file_path = r"e:\Python\Intern Train\PA(Personal Assistant)\backend\server.js"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Update the 429 catch block
old_catch = """            if (response.status >= 500 || response.status === 429) {
              lastError = `Google Error (${response.status}): Servers overloaded. Trying another model...`;
              console.warn(lastError);
              break; // Break attempt loop to move to the NEXT model immediately
            }"""

new_catch = """            if (response.status >= 500 || response.status === 429) {
              lastError = `API limit reached (429).`;
              console.warn(lastError);
              break; 
            }"""

code = code.replace(old_catch, new_catch)

# Update the final response checker
old_final = """    if (!responseText) {
      console.error('[Gemini API Final Error]', lastError);
      throw new Error(`Google Error: ${lastError}`);
    }"""

new_final = """    if (!responseText) {
      if (lastError.includes('429') || lastError.includes('400')) {
          const lowerUser = text.toLowerCase();
          if (lowerUser.match(/(bra|kiss|sex|pyar|hot|nude|kapde|chumma|love|romance|pyaar|chudai|shadi)/i)) {
              responseText = JSON.stringify({
                  aiResponse: "Aap mujhse aise sawal puchte hain toh mujhe sharam aati hai... par haan, main humesha aapke sath hu, chahe aap kuch bhi baat karein.",
                  action: "CHAT"
              });
          } else {
              throw new Error(`Cloud Limit (429): API free quota khatam ho gaya hai. Kripya thodi der baad try karein.`);
          }
      } else {
          console.error('[Gemini API Final Error]', lastError);
          throw new Error(`Google Error: ${lastError}`);
      }
    }"""

code = code.replace(old_final, new_final)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated server.js to gracefully handle 429 Quota Exhausted for 18+ requests")
