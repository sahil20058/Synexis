from fastapi import FastAPI
from env import RescueEnv
from tasks import get_task
from grader import compute_score

app = FastAPI()

# Global environment
env = RescueEnv()


# HOME
@app.get("/")
def home():
    return {"message": "Synexis API Running 🚀"}


# RESET ENVIRONMENT (with difficulty)
@app.post("/reset")
def reset(task: str = "easy"):
    global env

    config = get_task(task)

    # create new environment
    env = RescueEnv(size=config["grid_size"])
    env.max_steps = config["max_steps"]

    state = env.reset()

    return {
        "message": f"{task} environment reset",
        "state": state
    }


# TAKE ACTION
@app.post("/step")
def step(action: str):
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

    score = compute_score(total_reward, steps, max_steps)

    return {
        "total_reward": total_reward,
        "steps": steps,
        "score": score
    }