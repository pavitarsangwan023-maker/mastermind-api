const cron = require('node-cron');
const Memory = require('./models/Memory');

// This function starts the background scheduler
const startScheduler = () => {
  console.log("Mastermind Scheduler Started...");

  // Runs every minute to check for reminders
  // In a real app, 'node-cron' would be installed. Using setInterval simulation here.
  setInterval(async () => {
    try {
      console.log("[Scheduler] Checking memory for pending reminders...");
      
      // Real logic: Find memories where category is 'reminders' and time <= now
      // const pendingReminders = await Memory.find({ category: 'reminders', isCompleted: false });
      
      // Simulate finding a reminder
      const foundReminder = {
        _id: 'rem_12345',
        userText: 'Mujhe kal subah 9 baje meeting yaad dilana',
        aiResponse: 'Meeting time is up!',
        snoozeCount: 0
      };

      if (foundReminder) {
        triggerSmartVoiceAlert(foundReminder);
      }

    } catch (error) {
      console.error("[Scheduler Error]", error);
    }
  }, 60000); // Check every 60 seconds
};

// Generates a smart, context-aware spoken message based on the task
const generateVoicePrompt = (taskText) => {
  if (taskText.toLowerCase().includes('meeting')) {
    return `Sir, time ho gaya hai. Aapki meeting shuru hone wali hai.`;
  } else if (taskText.toLowerCase().includes('dawai') || taskText.toLowerCase().includes('medicine')) {
    return `Sir, aapki dawai lene ka time ho gaya hai. Kripya apna khayal rakhein.`;
  } else if (taskText.toLowerCase().includes('call')) {
    return `Sir, aapko ek zaroori call karni thi. Time ho gaya hai.`;
  } else {
    // Default smart response
    return `Sir, aapne mujhe yaad dilane ko kaha tha: ${taskText}`;
  }
};

const triggerSmartVoiceAlert = (reminder) => {
  const spokenMessage = generateVoicePrompt(reminder.userText);
  console.log(`\n🔊 [AI VOICE ALERT TRIGGERED]`);
  console.log(`Sending TTS Command to Phone: "${spokenMessage}"`);
  
  // In a real app, this sends the exact string `spokenMessage` via push notification.
  // The React Native app receives it and immediately plays it via expo-speech / TTS.
};

module.exports = { startScheduler };
