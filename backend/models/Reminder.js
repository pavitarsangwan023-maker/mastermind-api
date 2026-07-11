const mongoose = require('mongoose');

const reminderSchema = new mongoose.Schema({
  userEmail: { type: String, required: true },
  taskText: { type: String, required: true },
  dueDate: { type: Date, required: true },
  status: { type: String, enum: ['PENDING', 'COMPLETED', 'SNOOZED'], default: 'PENDING' },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Reminder', reminderSchema);
