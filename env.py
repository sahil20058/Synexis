import random
from fastapi import FastAPI
from pydantic import BaseModel

# =========================
# Environment Logic
# =========================

class RescueEnv:
    def __init__(self, size=5):
        self.size = size
        self.reset()

    def reset(self):
        # Agent position
        self.agent_pos = [0, 0]

        # Random victim position
        self.victim_pos = [
            random.randint(0, self.size - 1),
            random.randint(0, self.size - 1)
        ]

        # State variables
        self.steps = 0
        self.max_steps = 20
        self.done = False

        return self.get_state()

    def get_state(self):
        return {
            "agent_pos": self.agent_pos,
            "victim_pos": self.victim_pos,
            "steps": self.steps
        }

    def step(self, action):
        if self.done:
            return self.get_state(), 0.0, True

        # Move agent
        if action == "UP":
            self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
        elif action == "DOWN":
            self.agent_pos[0] = min(self.size - 1, self.agent_pos[0] + 1)
        elif action == "LEFT":
            self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
        elif action == "RIGHT":
            self.agent_pos[1] = min(self.size - 1, self.agent_pos[1] + 1)

        reward = -0.1  # step penalty

        # Check if rescued
        if self.agent_pos == self.victim_pos:
            reward = 1.0
            self.done = True

        self.steps += 1

        # End if max steps reached
        if self.steps >= self.max_steps:
            self.done = True

        return self.get_state(), reward, self.done


# =========================
# FastAPI Wrapper (IMPORTANT)
# =========================

app = FastAPI()

env = RescueEnv()

class ActionRequest(BaseModel):
    action: str


@app.post("/reset")
def reset():
    state = env.reset()
    return {
        "observation": state,
        "reward": 0.0,
        "done": False
    }


@app.post("/step")
def step(req: ActionRequest):
    state, reward, done = env.step(req.action)
    return {
        "observation": state,
        "reward": reward,
        "done": done
    }