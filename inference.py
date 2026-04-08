"""
Inference Script — Synexis Rescue Environment
=============================================
Uses OpenAI client to interact with the Synexis environment.
Emits [START], [STEP], [END] logs to stdout as required.

Environment variables:
    API_BASE_URL      The API endpoint for the LLM.
    MODEL_NAME        The model identifier to use for inference.
    HF_TOKEN          Your Hugging Face / API key.
"""

import os
import requests
from typing import List, Optional
from openai import OpenAI

# ── Environment variables ────────────────────────────────────────────────────
API_KEY      = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME",   "Qwen/Qwen2.5-72B-Instruct")
ENV_URL      = os.getenv("ENV_URL",      "https://sahil-2085-synexis.hf.space")
BENCHMARK    = "synexis"

# ── Config ───────────────────────────────────────────────────────────────────
TASKS        = ["easy", "medium", "hard"]
MAX_STEPS    = {"easy": 20, "medium": 25, "hard": 30}
TEMPERATURE  = 0.3
MAX_TOKENS   = 50

SYSTEM_PROMPT = """You are an AI agent navigating a grid to rescue a victim.
You can only move in 4 directions: UP, DOWN, LEFT, RIGHT.

You will be given:
- Your current position (row, col)
- The victim's position (row, col)

Strategy: Move toward the victim as directly as possible.
- If victim row < your row → UP
- If victim row > your row → DOWN
- If victim col < your col → LEFT
- If victim col > your col → RIGHT

Reply with ONLY one word: UP, DOWN, LEFT, or RIGHT. Nothing else."""


# ── Loggers ─────────────────────────────────────────────────────────────────
def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val  = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# ── Environment helpers ──────────────────────────────────────────────────────
def env_reset(task: str) -> dict:
    resp = requests.post(f"{ENV_URL}/reset", params={"task": task}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def env_step(action: str) -> dict:
    resp = requests.post(f"{ENV_URL}/step", params={"action": action}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def env_score() -> dict:
    resp = requests.get(f"{ENV_URL}/score", timeout=30)
    resp.raise_for_status()
    return resp.json()


# ── LLM action chooser ───────────────────────────────────────────────────────
def get_action(client: OpenAI, agent_pos: list, victim_pos: list, step: int) -> str:
    user_prompt = (
        f"Step: {step}\n"
        f"Your position: row={agent_pos[0]}, col={agent_pos[1]}\n"
        f"Victim position: row={victim_pos[0]}, col={victim_pos[1]}\n"
        "What is your next move?"
    )
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip().upper()
        # Extract valid action — take first word in case model adds extra text
        for word in text.split():
            if word in ("UP", "DOWN", "LEFT", "RIGHT"):
                return word
        # Fallback: compute action directly if model gives invalid response
        return fallback_action(agent_pos, victim_pos)
    except Exception as exc:
        print(f"[DEBUG] LLM call failed: {exc}", flush=True)
        return fallback_action(agent_pos, victim_pos)


def fallback_action(agent_pos: list, victim_pos: list) -> str:
    """Simple heuristic: move toward victim."""
    if victim_pos[0] < agent_pos[0]:
        return "UP"
    elif victim_pos[0] > agent_pos[0]:
        return "DOWN"
    elif victim_pos[1] < agent_pos[1]:
        return "LEFT"
    else:
        return "RIGHT"


# ── Single task runner ───────────────────────────────────────────────────────
def run_task(client: OpenAI, task: str) -> None:
    log_start(task=task, env=BENCHMARK, model=MODEL_NAME)

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    try:
        # Reset environment
        result   = env_reset(task)
        state    = result.get("state", {})
        max_steps = MAX_STEPS[task]

        for step in range(1, max_steps + 1):
            agent_pos  = state.get("agent_pos",  [0, 0])
            victim_pos = state.get("victim_pos", [0, 0])

            action = get_action(client, agent_pos, victim_pos, step)

            try:
                step_result = env_step(action)
                state  = step_result.get("state",  {})
                reward = float(step_result.get("reward", -0.1))
                done   = bool(step_result.get("done",   False))
                error  = None
            except Exception as e:
                reward = -0.1
                done   = False
                error  = str(e)

            rewards.append(reward)
            steps_taken = step
            log_step(step=step, action=action, reward=reward, done=done, error=error)

            if done:
                break

        # Get final score from /score endpoint
        try:
            score_data = env_score()
            score      = float(score_data.get("score", 0.0))
        except Exception:
            # Fallback: compute score manually
            total_reward = sum(rewards)
            score = max(0.0, min(1.0, (total_reward + steps_taken * 0.1) / steps_taken)) if steps_taken > 0 else 0.0

        score   = max(0.0, min(1.0, score))   # clamp to [0, 1]
        success = score > 0.0 and any(r == 1.0 for r in rewards)

    except Exception as exc:
        print(f"[DEBUG] Task '{task}' error: {exc}", flush=True)

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


# ── Main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    for task in TASKS:
        print(f"\n{'='*50}", flush=True)
        print(f"Running task: {task.upper()}", flush=True)
        print(f"{'='*50}", flush=True)
        run_task(client, task)


if __name__ == "__main__":
    main()