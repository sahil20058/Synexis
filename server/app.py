# server/app.py
from fastapi import FastAPI, Body
from typing import Literal
from server.environment import RescueEnv
from tasks import get_task
from grader import compute_score
import uvicorn

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
    raw_score = compute_score(env.total_reward, env.steps, env.max_steps)
    epsilon = 1e-4
    score_value = max(min(raw_score, 1.0 - epsilon), epsilon)
    return {"score": score_value}

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=True)

if __name__ == "__main__":
    main()
