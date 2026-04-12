# grader.py

def compute_score(total_reward, steps, max_steps):
    """
    Robust score function:
    - Handles negative rewards
    - Always returns strictly between (0,1)
    """

    # Normalize reward into positive range
    # Worst case: all penalties → total_reward ≈ -max_steps*0.1
    min_reward = -max_steps * 0.1
    max_reward = 1.0  # best case rescue

    # Normalize to 0 → 1
    score = (total_reward - min_reward) / (max_reward - min_reward)

    # Final strict clipping
    epsilon = 1e-4
    score = max(min(score, 1 - epsilon), epsilon)

    return score
