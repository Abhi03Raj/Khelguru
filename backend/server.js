require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bcrypt = require('bcrypt');

const app = express();
app.use(cors());
app.use(express.json());

mongoose.connect(process.env.MONGO_URL)
  .then(() => console.log("✅ Connected to MongoDB"))
  .catch(err => console.error("❌ MongoDB error:", err));

// -------------------- User Schema --------------------
const userSchema = new mongoose.Schema({
  username: String,
  password: String,
  history: [new mongoose.Schema({
    kdRatio: Number,
    avgDamage: Number,
    avgSurvivalTime: Number,
    winRatio: Number,
    headshotPercentage: Number,
    tier: String,
    tips: [String],
    drills: [String],
    timestamp: String
  }, { _id: false })]
});
const User = mongoose.model('User', userSchema);

// -------------------- Tier Progress Schema --------------------
const tierProgressSchema = new mongoose.Schema({
  username: String,
  season: String,
  tier: String,
  tierStage: Number,
  tierPoints: Number,
  updatedAt: { type: Date, default: Date.now }
});
const TierProgress = mongoose.model('TierProgress', tierProgressSchema);

// -------------------- Auth: Register --------------------
app.post('/register', async (req, res) => {
  const { username, password } = req.body;
  if (await User.findOne({ username })) {
    return res.status(400).json({ message: 'User already exists' });
  }
  const hashed = await bcrypt.hash(password, 10);
  await User.create({ username, password: hashed, history: [] });
  res.json({ message: 'Registered', user: { username } });
});

// -------------------- Auth: Login --------------------
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ username });
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ message: 'Invalid credentials' });
  }
  res.json({ message: 'Login successful', user: { username } });
});

// -------------------- Save Match Stats --------------------
app.post('/save-stats', async (req, res) => {
  const { username, stats } = req.body;
  const user = await User.findOne({ username });
  if (!user) return res.status(404).json({ message: 'User not found' });

  user.history.unshift(stats); // push new stats to front
  if (user.history.length > 50) user.history.pop(); // optional limit
  await user.save();

  res.json({ message: 'Stats saved' });
});

// -------------------- Get User History --------------------
app.get('/api/user/history/:username', async (req, res) => {
  const user = await User.findOne({ username: req.params.username });
  if (!user) return res.status(404).json({ history: [] });
  const latest5 = user.history.slice(0, 5);
  res.json(latest5);
});

// -------------------- Save/Update Tier Progress --------------------
app.post('/api/tier-progress', async (req, res) => {
  const { username, season, tier, tierStage, tierPoints } = req.body;
  if (!username || !season || !tier) {
    return res.status(400).json({ message: 'Missing required fields' });
  }

  let record = await TierProgress.findOne({ username, season });
  if (record) {
    record.tier = tier;
    record.tierStage = tierStage;
    record.tierPoints = tierPoints;
    record.updatedAt = new Date();
    await record.save();
  } else {
    await TierProgress.create({ username, season, tier, tierStage, tierPoints });
  }

  res.json({ message: 'Tier progress saved/updated' });
});

// -------------------- Get Tier Progress --------------------
app.get('/api/tier-progress/:username', async (req, res) => {
  const username = req.params.username;
  const data = await TierProgress.find({ username });
  if (!data.length) {
    return res.status(404).json({ message: 'No tier progress found' });
  }
  res.json(data);
});

// -------------------- Server Start --------------------
app.listen(5000, () => {
  console.log('🚀 Server running on port 5000');
});
