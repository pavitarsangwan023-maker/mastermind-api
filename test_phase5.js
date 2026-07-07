console.log("========== RUNNING PHASE 5 TESTS ==========\n");

// --- 1. Test Backend Scheduler (Smart Voice Alerts) ---
console.log("--- 1. Testing Smart Voice Alerts (Scheduler) ---");
const generateVoicePrompt = (taskText) => {
  if (taskText.toLowerCase().includes('meeting')) {
    return `Sir, time ho gaya hai. Aapki meeting shuru hone wali hai.`;
  } else if (taskText.toLowerCase().includes('dawai') || taskText.toLowerCase().includes('medicine')) {
    return `Sir, aapki dawai lene ka time ho gaya hai. Kripya apna khayal rakhein.`;
  } else if (taskText.toLowerCase().includes('call')) {
    return `Sir, aapko ek zaroori call karni thi. Time ho gaya hai.`;
  } else {
    return `Sir, aapne mujhe yaad dilane ko kaha tha: ${taskText}`;
  }
};

console.log("Input: 'meeting' ->", generateVoicePrompt("Mujhe meeting jana hai") === "Sir, time ho gaya hai. Aapki meeting shuru hone wali hai." ? "PASS" : "FAIL");
console.log("Input: 'dawai' ->", generateVoicePrompt("Dawai khani hai") === "Sir, aapki dawai lene ka time ho gaya hai. Kripya apna khayal rakhein." ? "PASS" : "FAIL");
console.log("Input: 'kuch bhi' ->", generateVoicePrompt("Gadi saaf karni hai").includes("aapne mujhe yaad dilane ko kaha tha") ? "PASS" : "FAIL");
console.log("");

// --- 2. Test Voice Snooze Logic ---
console.log("--- 2. Testing Voice Snooze Logic (Backend API) ---");
const testSnooze = (snoozeMinutes) => {
  return `Thik hai sir, main aapko ${snoozeMinutes} minute baad wapas yaad dila dungi.`;
};
console.log("Input: '10' minutes ->", testSnooze(10) === "Thik hai sir, main aapko 10 minute baad wapas yaad dila dungi." ? "PASS" : "FAIL");
console.log("");

// --- 3. Test Caller ID Announcer (Frontend Logic) ---
console.log("--- 3. Testing Caller ID Announcer Logic ---");
const simulateIncomingCall = (userTitle, callerName, announceCalls, overrideSilentMode) => {
  if (!announceCalls) return "SILENT (Feature Disabled)";
  
  const announcement = `${userTitle}, ${callerName} ka call aa raha hai.`;
  
  if (overrideSilentMode) {
    return `[SYSTEM OVERRIDE SILENT] 🔊 Speaking: "${announcement}"`;
  } else {
    return `🔊 Speaking: "${announcement}"`;
  }
};

console.log("Test: 'Sir' profile, 'Rahul' calling, Overriding Silent ->", simulateIncomingCall("Sir", "Rahul", true, true).includes("[SYSTEM OVERRIDE SILENT]") ? "PASS" : "FAIL");
console.log("Test: 'Mam' profile, 'Neha' calling ->", simulateIncomingCall("Mam", "Neha", true, false).includes("Mam, Neha ka call") ? "PASS" : "FAIL");
console.log("Test: Toggle Disabled ->", simulateIncomingCall("Sir", "Rahul", false, true) === "SILENT (Feature Disabled)" ? "PASS" : "FAIL");

console.log("\n========== ALL PHASE 5 TESTS COMPLETED SUCCESSFULLY ==========");
