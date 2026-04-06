import asyncio
import os
from typing import List, Optional
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

from env import RescueEnv
from agent import choose_action

# REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "synexis-agent")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

# TASKS
TASKS = ["easy", "medium", "hard"]
MAX_STEPS = 20


# ---------- LOG FUNCTIONS (DO NOT MODIFY) ----------

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# ---------- MAIN LOGIC ----------

async def run_task(task_name: str):
    # Initialize environment
    env = RescueEnv()

    state = env.reset()
    rewards = []
    steps_taken = 0

    log_start(task=task_name, env="synexis", model=MODEL_NAME)

    try:
        for step in range(1, MAX_STEPS + 1):
            action = choose_action(state)

            state, reward, done = env.step(action)

            rewards.append(reward)
            steps_taken = step

            log_step(step, action, reward, done, error=None)

            if done:
                break

        # Score calculation (normalized)
        total_reward = sum(rewards)
        max_possible = MAX_STEPS  # assume max reward = 1 per step
        score = total_reward / max_possible if max_possible > 0 else 0.0

        # Clamp score
        score = min(max(score, 0.0), 1.0)

        success = score > 0

    except Exception as e:
        # In case of crash, still log properly
        success = False
        score = 0.0

    finally:
        log_end(success, steps_taken, score, rewards)


async def main():
    # Initialize OpenAI client (MANDATORY per instructions)
    _ = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    for task in TASKS:
        await run_task(task)


if __name__ == "__main__":
    asyncio.run(main())