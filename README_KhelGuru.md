# 🎮 KhelGuru: AI-Powered Player Performance Analysis and Coaching System for BGMI

> **Level up your BGMI gameplay with AI-driven coaching, personalized feedback, promotion readiness tracking, and performance analytics.**

---

## 📌 Overview

**KhelGuru** is a web-based application built to analyze and improve the performance of BGMI (Battlegrounds Mobile India) players using Artificial Intelligence. The platform offers personalized drills, tips, promotion readiness detection, tier tracking, and profile-based analytics—making it a personal e-coach for every player, from casual to competitive.

---

## 🧠 Core Features

- ✅ **Submit Your Match Stats**: Input stats like K/D ratio, average damage, survival time, headshot %, etc.
- 📊 **Spider Graph Comparison**: Visual comparison between your stats and standard tier benchmarks.
- 🤖 **ML-Based Promotion Prediction**: Machine Learning determines if you're ready for tier promotion.
- 💡 **AI Tips & Drills**: Get dynamic training tips and practice drills based on your weaknesses.
- 🧬 **Weekly Goal Generator**: Personalized improvement targets based on recent performance.
- 📂 **History & Trend Tracker**: See your improvement over time through charts and tables.
- 🏆 **Premium Tier Progression Tracker**: Manually input your tier stage and points for deeper tracking (for premium users).
- 🔐 **User Authentication**: Register/Login to track and save your stats securely.

---

## 🛠️ Tech Stack

| Layer         | Technology Used                    | Purpose                                      |
|---------------|-------------------------------------|----------------------------------------------|
| Frontend      | React.js, Bootstrap                | UI rendering, user input, and interaction    |
| Backend (AI)  | Flask, Scikit-learn, Pandas        | Data processing, ML prediction, API          |
| Backend (Auth)| Express.js, MongoDB, Mongoose      | User management, stat history storage        |
| ML Model      | Trained with CSV data              | Predict promotion readiness                  |
| Storage       | player_data_1000.csv, MongoDB      | Local CSV and cloud DB support               |

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/khelguru.git
cd khelguru
```

### 2. Set Up Python (Backend)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 3. Set Up Node.js (Express Server)

```bash
cd backend
npm install
node server.js
```

### 4. Run React Frontend

```bash
cd frontend
npm install
npm start
```

> Make sure MongoDB is running and environment variables (`.env`) are set for Express backend.

---

## 📁 File Structure

```
/backend
  ├── app.py                # Flask ML API
  ├── train_stats.py        # Model training script
  ├── player_data_1000.csv  # Player stats CSV
  ├── server.js             # Express backend
/frontend
  ├── App.js                # Main React app
  ├── components/
      ├── PlayerInput.js
      ├── Profile.js
      ├── Tips.js, Drills.js
      ├── TierProgressInput.js
```

---

## 📷 Screenshots

## 📊 Dashboard Preview

![Dashboard](my-app/assets/Dashboard.jpg)

## 🧠 Tips and Drills

![Tips and Drills](my-app/assets/tips_and_drills.jpg)

## 🕸️ Spider Chart Comparison

![Spider Chart](my-app/assets/spider_chart_comaparision.jpg)

## 📁 User History View

![User History](my-app/assets/user_history.jpg)

## 🔄 System Flowchart

![Flowchart](my-app/assets/flowchart.jpg)


---

## 📈 ML Model

- **Model**: Logistic Regression Classifier
- **Input Features**:
  - K/D Ratio
  - Average Damage
  - Average Survival Time
  - Win Rate %
  - Headshot %
  - Tier (mapped to numerical value)
- **Output**: `Promotion Ready: True/False`

---

## 🛡️ Security

- Passwords are hashed with `bcrypt`
- User sessions are stored securely
- Input validation is enforced on frontend and backend

---

## 🧪 Testing

- Tested with both valid and invalid data
- Postman used for API testing
- Manual UI validation via browser

---

## 📌 Future Scope

- 🎮 Real-time API integration with game logs (if available)
- 📱 Mobile app version with notifications
- 🎥 Replay-based analysis using computer vision
- 💳 Payment gateway for premium subscriptions

---

## 🤝 Contributors

- 👤 Abhishek Raj – Developer, Designer, ML Trainer
- 💬 ChatGPT – Support in Architecture, Code Generation, Documentation

---

## 📄 License

This project is a part of an academic submission and is free to use for learning and educational purposes. Commercial usage requires explicit permission.