const cron = require('node-cron');
const { Expo } = require('expo-server-sdk');
const Reminder = require('./models/Reminder');
const User = require('./models/User');

const expo = new Expo();

const startScheduler = () => {
  console.log("Mastermind Scheduler Started...");

  // Check every 60 seconds
  setInterval(async () => {
    try {
      console.log("[Scheduler] Checking memory for pending reminders...");
      
      const now = new Date();
      // Find reminders that are due or overdue, and are still PENDING
      const pendingReminders = await Reminder.find({ 
          dueDate: { $lte: now }, 
          status: 'PENDING' 
      });

      if (pendingReminders.length === 0) return;

      console.log(`[Scheduler] Found ${pendingReminders.length} pending reminders!`);

      // Group reminders by userEmail to avoid spamming the database
      for (const reminder of pendingReminders) {
          try {
              const user = await User.findOne({ email: reminder.userEmail });
              if (user && user.expoPushToken && Expo.isExpoPushToken(user.expoPushToken)) {
                  // Send Push Notification
                  const spokenMessage = generateVoicePrompt(reminder.taskText);
                  
                  let messages = [{
                    to: user.expoPushToken,
                    sound: 'default',
                    priority: 'high',
                    title: reminder.taskText.length > 40 ? reminder.taskText.substring(0, 40) + '...' : reminder.taskText,
                    body: spokenMessage,
                    data: { action: 'REMINDER_ALARM', text: spokenMessage },
                  }];
                  
                  let chunks = expo.chunkPushNotifications(messages);
                  for (let chunk of chunks) {
                      await expo.sendPushNotificationsAsync(chunk);
                  }
                  
                  console.log(`🔊 Push Notification sent to ${user.email} for reminder: ${reminder.taskText}`);
              } else {
                  console.log(`⚠️ Push token not found or invalid for user: ${reminder.userEmail}`);
              }
              
              // Mark as completed regardless so it doesn't loop infinitely
              reminder.status = 'COMPLETED';
              await reminder.save();
              
          } catch (err) {
              console.error("[Scheduler Error on specific reminder]", err);
          }
      }

    } catch (error) {
      console.error("[Scheduler Error]", error);
    }
  }, 60000); 
};

// Generates a smart, context-aware spoken message based on the task
const generateVoicePrompt = (taskText) => {
  if (taskText.toLowerCase().includes('meeting')) {
    return `Sir, time ho gaya hai. Aapki meeting shuru hone wali hai.`;
  } else if (taskText.toLowerCase().includes('dawai') || taskText.toLowerCase().includes('medicine') || taskText.toLowerCase().includes('pills')) {
    return `Sir, aapki dawai lene ka time ho gaya hai. Kripya apna khayal rakhein.`;
  } else if (taskText.toLowerCase().includes('call')) {
    return `Sir, aapko ek zaroori call karni thi. Time ho gaya hai.`;
  } else {
    // Default smart response
    return `Sir, aapka time ho gaya hai. Aapne kaha tha: ${taskText}`;
  }
};

module.exports = { startScheduler };
