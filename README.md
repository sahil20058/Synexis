# 🤖 Synexis — Grid Rescue RL Environment

> An OpenEnv-compatible reinforcement learning environment where an AI agent navigates a 5×5 grid to locate and rescue a randomly placed victim, built with FastAPI and deployable via Docker or Hugging Face Spaces.

[![OpenEnv](https://img.shields.io/badge/OpenEnv-compatible-brightgreen)](https://github.com/meta-pytorch/OpenEnv)
[![Hugging Face](https://img.shields.io/badge/HuggingFace-Space-orange)](https://sahil-2085-synexis.hf.space)
[![Docker](https://img.shields.io/badge/Docker-ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-powered-teal)](https://fastapi.tiangolo.com/)

---

## 📖 Overview

**Synexis** is a grid-based rescue simulation environment built for reinforcement learning (RL) post-training. An agent starts at position `[0, 0]` on a 5×5 grid and must navigate using directional actions to find a **randomly placed victim** within 20 steps.

It follows the standard [OpenEnv](https://github.com/meta-pytorch/OpenEnv) interface — `reset()`, `step()`, `state()` — making it a drop-in environment for RL frameworks like TRL, Oumi, and others.

| Property | Value |
|---|---|
| Grid Size | 5×5 (configurable) |
| Agent Start | `[0, 0]` |
| Victim Position | Random (never `[0, 0]`) |
| Max Steps | 20 per episode |
| Actions | `UP`, `DOWN`, `LEFT`, `RIGHT` |
| Rescue Reward | `+1.0` |
| Step Penalty | `-0.1` per step |
| Interface | OpenEnv-compatible (`reset`, `step`, `state`) |
| Deployment | Docker · Hugging Face Spaces · Local |

---

## ✨ Features

- 🧭 **Grid navigation** — Agent moves through a 2D environment using cardinal directions with boundary clamping
- 🎯 **Rescue objective** — `+1.0` reward when agent reaches the victim's position
- ⏱️ **Step penalty** — `-0.1` per step to encourage efficient paths
- 🔀 **Random victim placement** — Victim spawns at a random position (never at agent start) each episode
- 🔁 **Episode management** — Automatic tracking of steps, total reward, and done state
- ⚡ **FastAPI server** — REST endpoints following the OpenEnv spec
- 🐳 **Docker-ready** — One-command container builds and deployments
- ☁️ **Hugging Face Spaces** — Live deployment with an interactive `/docs` UI
- ✅ **OpenEnv validated** — Passes all official OpenEnv validation checks

---

## 🚀 Quick Start

The simplest way to interact with Synexis is via HTTP requests against the running server.

### Using `requests`

```python
import requests

BASE_URL = "https://sahil-2085-synexis.hf.space"

# Reset the environment
response = requests.post(f"{BASE_URL}/reset", json={"task": "rescue"})
state = response.json()
print(f"Agent:  {state['agent_pos']}")
print(f"Victim: {state['victim_pos']}")
print(f"Steps:  {state['steps']} / {state['max_steps']}")

# Take actions
for action in ["DOWN", "DOWN", "RIGHT", "RIGHT", "DOWN"]:
    response = requests.post(f"{BASE_URL}/step", json={"action": action})
    result = response.json()
    print(f"Action: {action}")
    print(f"  → Agent pos: {result['state']['agent_pos']}")
    print(f"  → Reward:    {result['reward']}")
    print(f"  → Done:      {result['done']}")
    if result['done']:
        break

# Get total accumulated score
score = requests.get(f"{BASE_URL}/score").json()
print(f"Total reward: {score}")
```

### Connect to Local Server

```python
import requests

BASE_URL = "http://localhost:8000"

# Reset
state = requests.post(f"{BASE_URL}/reset", json={"task": "rescue"}).json()

# Step
result = requests.post(f"{BASE_URL}/step", json={"action": "RIGHT"}).json()
print(result)
```

---

## 📦 Installation

### Prerequisites

- Python 3.10+
- Docker (for containerized use)
- `uv` (recommended) or `pip`

### Install from Source

```bash
git clone https://github.com/sahil20058/Synexis.git
cd Synexis
pip install -e .
```

### Install with `uv`

```bash
uv pip install -e .
```

### Install Dependencies Only

```bash
pip install -r requirements.txt
```

---

## 🐳 Docker

### Build the Image

```bash
docker build -t synexis:latest .
```

### Run the Container

```bash
docker run -p 8000:8000 synexis:latest
```

The server will be available at `http://localhost:8000`.

---

## 🌐 Live Deployment

The environment is live on Hugging Face Spaces:

| Resource | Link |
|---|---|
| 🔗 Environment Server | [sahil-2085-synexis.hf.space](https://sahil-2085-synexis.hf.space) |
| 📄 Interactive API Docs | [sahil-2085-synexis.hf.space/docs](https://sahil-2085-synexis.hf.space/docs) |

---

## 🔌 API Reference

All endpoints follow the OpenEnv HTTP specification.

---

### 🔹 Reset Environment

Initialises a new episode. Places the agent at `[0, 0]` and the victim at a random position.

```http
POST /reset
```

**Request Body:**
```json
{
  "task": "rescue"
}
```

**Response:**
```json
{
  "agent_pos": [0, 0],
  "victim_pos": [3, 4],
  "steps": 0,
  "max_steps": 20,
  "done": false
}
```

---

### 🔹 Step

Send an action and receive the updated state, reward, and done flag.

```http
POST /step
```

**Request Body:**
```json
{
  "action": "RIGHT"
}
```

**Valid Actions:** `UP` · `DOWN` · `LEFT` · `RIGHT`

**Response:**
```json
{
  "state": {
    "agent_pos": [0, 1],
    "victim_pos": [3, 4],
    "steps": 1,
    "max_steps": 20,
    "done": false
  },
  "reward": -0.1,
  "done": false
}
```

> ✅ **Rescue:** When `agent_pos == victim_pos`, reward is `+1.0` and `done` is `true`.
> ⏱️ **Timeout:** When `steps >= 20`, `done` is set to `true`.

---

### 🔹 Get Score

Returns the accumulated `total_reward` for the current episode.

```http
GET /score
```

---

### 🔹 Check Status

Returns server health and readiness.

```http
GET /status
```

---

## 🏗️ Data Models

### `ActionRequest`

| Field | Type | Description |
|---|---|---|
| `action` | `str` | One of `UP`, `DOWN`, `LEFT`, `RIGHT` |

### `ResetRequest`

| Field | Type | Description |
|---|---|---|
| `task` | `str` | Task identifier (e.g. `"rescue"`) |

### State (returned by `reset` and `step`)

| Field | Type | Description |
|---|---|---|
| `agent_pos` | `List[int]` | Agent's current `[row, col]` position |
| `victim_pos` | `List[int]` | Victim's `[row, col]` position |
| `steps` | `int` | Number of steps taken this episode |
| `max_steps` | `int` | Maximum steps allowed (default: `20`) |
| `done` | `bool` | Whether the episode has ended |

---

## 🎮 Environment Logic

### Movement

The agent moves one cell at a time. Movement is **clamped** to grid boundaries — the agent cannot move outside the 5×5 grid.

```
Action  →  Effect
──────────────────────────────────────────────
UP      →  agent_pos[0] -= 1  (clamped min 0)
DOWN    →  agent_pos[0] += 1  (clamped max 4)
LEFT    →  agent_pos[1] -= 1  (clamped min 0)
RIGHT   →  agent_pos[1] += 1  (clamped max 4)
```

### Reward Structure

```
+1.0   →  Agent reaches victim position  (rescue!)
-0.1   →  Every step taken               (encourages efficiency)
```

### Episode Termination

An episode ends when either condition is met:

- ✅ The agent reaches the victim (`agent_pos == victim_pos`) → reward `+1.0`
- ⏱️ The step count reaches `max_steps` (default: `20`) → no bonus reward

---

## 📁 Project Structure

```
Synexis/
├── server/
│   ├── __init__.py          # Server module exports
│   ├── app.py               # FastAPI application & route definitions
│   └── environment.py       # RescueEnv — core grid environment logic
├── agent.py                 # Example RL agent implementation
├── client.py                # HTTP client utilities
├── grader.py                # Reward & scoring logic
├── tasks.py                 # Episode task definitions
├── inference.py             # Model inference utilities
├── models.py                # ActionRequest, ResetRequest Pydantic models
├── openenv.yaml             # OpenEnv environment metadata
├── Dockerfile               # Container image definition
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Package configuration
├── uv.lock                  # Locked dependency versions
└── README.md                # This file
```

---

## 🧪 Testing

### Test Core Logic Directly

```python
from server.environment import RescueEnv

env = RescueEnv(size=5)

# Test reset
state = env.reset()
assert state["agent_pos"] == [0, 0]
assert state["victim_pos"] != [0, 0]
assert state["steps"] == 0
assert state["done"] == False

# Test step
state, reward, done = env.step("RIGHT")
assert state["agent_pos"] == [0, 1]
assert reward == -0.1
assert state["steps"] == 1

print("All tests passed ✅")
```

### Test via cURL

```bash
# Reset
curl -X POST https://sahil-2085-synexis.hf.space/reset \
     -H "Content-Type: application/json" \
     -d '{"task": "rescue"}'

# Step
curl -X POST https://sahil-2085-synexis.hf.space/step \
     -H "Content-Type: application/json" \
     -d '{"action": "RIGHT"}'

# Score
curl https://sahil-2085-synexis.hf.space/score

# Status
curl https://sahil-2085-synexis.hf.space/status
```

---

## ✅ Validation

Synexis has been verified against the official OpenEnv validation suite:

```bash
openenv validate .
```

| Check | Status |
|---|---|
| OpenEnv spec compliance | ✅ Passed |
| Docker build | ✅ Successful |
| `/reset` endpoint | ✅ Functional |
| `/step` endpoint | ✅ Functional |
| `/score` endpoint | ✅ Functional |
| `/status` endpoint | ✅ Functional |
| Rescue reward (`+1.0`) | ✅ Verified |
| Step penalty (`-0.1`) | ✅ Verified |
| Timeout termination (`steps >= 20`) | ✅ Verified |

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| 🐍 Python 3.10+ | Core language |
| ⚡ FastAPI | HTTP server & API endpoints |
| 🤖 OpenEnv | Environment interface standard |
| ☁️ Hugging Face Spaces | Live cloud deployment |
| 🐳 Docker | Containerisation & reproducibility |

---

## 🔮 Future Improvements

- [ ] Add obstacles and dynamic terrain to increase environment complexity
- [ ] Implement advanced RL agents (PPO, DQN, A3C)
- [ ] Visualisation dashboard for episode replay
- [ ] Multi-agent coordination and competitive modes
- [ ] Configurable grid sizes and victim counts
- [ ] Delayed reward and trajectory-based scoring

---

## 🏁 Conclusion

Synexis demonstrates how AI agents can efficiently solve navigation and rescue problems using structured, standardised environments. Built on the OpenEnv framework with a clean `RescueEnv` core, it serves as a solid foundation for experimenting with more advanced real-world AI simulations and RL training pipelines.

---

## 🙌 Acknowledgements

Developed during the **OpenEnv Hackathon** organised by [Scaler Academy](https://www.scaler.com/), sponsored by:

- 🔥 [Meta PyTorch](https://pytorch.org/)
- 🤗 [Hugging Face](https://huggingface.co/)
- ⚡ PyTorch Community

---

## 👥 Team

**🧠 Team Name: Mind Matrix**

| Name | Role | Institution |
|---|---|---|
| Sahil Khan | Team Lead | Haldia Institute of Technology |
| Pritam Maity | Member | Haldia Institute of Technology |

---

## 📄 License

This project is open-source. See [LICENSE](./LICENSE) for details.
