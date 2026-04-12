# grader.py
def compute_score(total_reward, steps, max_steps):
    """
    Compute the score for the agent.
    Ensures score is strictly between 0 and 1 for all tasks.
    """
    # Basic score calculation
    score = total_reward / max_steps

    # Clip strictly between 0 and 1
    epsilon = 1e-4  # small buffer
    score = max(min(score, 1.0 - epsilon), epsilon)

    return score
