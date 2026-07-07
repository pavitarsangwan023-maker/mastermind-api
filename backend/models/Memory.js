const mongoose = require('mongoose');

const MemorySchema = new mongoose.Schema({
  userText: {
    type: String,
    required: true,
  },
  aiResponse: {
    type: String,
    required: true,
  },
  category: {
    type: String,
    enum: ['reminders', 'general', 'secrets', 'ideas'],
    default: 'general',
  },
  timestamp: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Memory', MemorySchema);
