---
title: Synexis
emoji: 🐨
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: 'AI-powered rescue environment with agent-based decision'
---

# 🚀 Synexis Rescue Environment

🧠 **Team: MindMatrix**

---

## 👥 Team Members

- Sahil Khan (Team Lead)
- Pritam Maity

🎓 Haldia Institute of Technology
📚 3rd Year Students

---

## 🌟 Project Overview

Synexis is an AI-powered rescue environment designed to simulate a grid-based search-and-rescue mission. An intelligent agent navigates a grid to locate and rescue a victim in the shortest possible time.

The project is built to integrate seamlessly with OpenEnv validation and supports dynamic difficulty levels.

---

## 🎯 Objectives

- Build a scalable and interactive AI environment
- Simulate real-world rescue navigation problems
- Enable agent-based decision making
- Provide API endpoints for external interaction and evaluation

---

## ⚙️ Features

- 🔹 Grid-based environment simulation
- 🔹 3 difficulty levels: Easy, Medium, Hard
- 🔹 FastAPI backend for real-time interaction
- 🔹 Step-by-step agent control
- 🔹 Score calculation system
- 🔹 Fully compatible with OpenEnv validation

---

## 🧠 How It Works

- The agent starts at position `(0,0)`
- A victim is randomly placed in the grid
- The agent can move in four directions: `UP`, `DOWN`, `LEFT`, `RIGHT`
- Each step has a small penalty
- Reaching the victim gives a reward

🎯 **Goal:** Rescue the victim in minimum steps

---

## 📡 API Endpoints

### 🔹 Reset Environment

```http
POST /reset
```

```json
{
  "task": "easy"
}
```

### 🔹 Take Action

```http
POST /step
```

```json
{
  "action": "RIGHT"
}
```

### 🔹 Get Score

```http
GET /score
```

### 🔹 Check Status

```http
GET /status
```

---

## 🌐 Live Deployment

🔗 **Hugging Face Space:** https://sahil-2085-synexis.hf.space

🔗 **API Docs:** https://sahil-2085-synexis.hf.space/docs

---

## 🛠️ Tech Stack

- 🐍 Python
- ⚡ FastAPI
- 🤖 OpenEnv
- ☁️ Hugging Face Spaces
- 🐳 Docker

---

## 📂 Project Structure
Synexis/
├── main.py
├── env.py
├── tasks.py
├── grader.py
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
└── README.md

---

## ✅ Validation

✔ Successfully passes OpenEnv validation
✔ Docker build successful
✔ API endpoints fully functional

---

## 🚀 Future Improvements

- Add obstacles and dynamic environments
- Implement advanced RL agents
- Visualization dashboard
- Multi-agent coordination

---

## 🏁 Conclusion

Synexis demonstrates how AI agents can efficiently solve navigation and rescue problems using structured environments. It serves as a foundation for more advanced real-world AI simulations.

---

## 🙌 Acknowledgement

Developed during the OpenEnv Hackathon organised by Scaler Academy and sponsored by Meta, PyTorch, and Hugging Face.
