from fastapi import FastAPI
from env import RescueEnv
from tasks import get_task
from grader import compute_score
from fastapi import Body
from typing import Literal

app = FastAPI()

# Global environment
env = RescueEnv()
env.difficulty = "easy"  # default difficulty


# HOME
@app.get("/")
def home():
    return {"message": "Synexis API Running 🚀"}


# RESET ENVIRONMENT (with difficulty)
@app.post("/reset")
def reset(task: Literal["easy", "medium", "hard"] = Body("easy")):
    global env

    # Validate difficulty level
    valid_tasks = ["easy", "medium", "hard"]
    if task not in valid_tasks:
        return {
            "error": f"Invalid difficulty '{task}'. Choose from: easy, medium, hard"
        }

    config = get_task(task)

    # Create new environment with config
    env = RescueEnv(size=config["grid_size"])
    env.max_steps = config["max_steps"]
    env.difficulty = task  # store difficulty on env

    state = env.reset()

    return {
        "message": f"{task} environment reset",
        "difficulty": task,
        "grid_size": config["grid_size"],
        "max_steps": config["max_steps"],
        "state": state
    }


# TAKE ACTION
@app.post("/step")
def step(action: Literal["UP", "DOWN", "LEFT", "RIGHT"] = Body(...)):
    state, reward, done = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done
    }


# GET SCORE
@app.get("/score")
def get_score():
    total_reward = getattr(env, "total_reward", 0)
    steps = getattr(env, "steps", 0)
    max_steps = env.max_steps
    difficulty = getattr(env, "difficulty", "easy")
    score = compute_score(total_reward, steps, max_steps)

    return {
        "difficulty": difficulty,
        "total_reward": total_reward,
        "steps": steps,
        "max_steps": max_steps,
        "score": score
    }


# GET CURRENT ENVIRONMENT STATUS
@app.get("/status")
def status():
    return {
        "difficulty": getattr(env, "difficulty", "easy"),
        "grid_size": env.size,
        "max_steps": env.max_steps,
        "steps": getattr(env, "steps", 0),
    }