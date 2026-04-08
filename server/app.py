from fastapi import FastAPI, Body
from typing import Literal
from server.environment import RescueEnv
from tasks import get_task
from grader import compute_score

app = FastAPI()

env = RescueEnv()

@app.get("/")
def home():
    return {"message": "Synexis API Running 🚀"}

@app.post("/reset")
def reset(task: Literal["easy","medium","hard"] = Body("easy")):
    global env
    config = get_task(task)
    env = RescueEnv(size=config["grid_size"])
    env.max_steps = config["max_steps"]
    env.difficulty = task
    state = env.reset()
    return {"state": state}

@app.post("/step")
def step(action: Literal["UP","DOWN","LEFT","RIGHT"] = Body(...)):
    state, reward, done = env.step(action)
    return {"state": state, "reward": reward, "done": done}

@app.get("/score")
def score():
    return {
        "score": compute_score(
            env.total_reward,
            env.steps,
            env.max_steps
        )
    }