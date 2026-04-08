def compute_score(total_reward, steps, max_steps):
    """
    Compute the score for the agent.
    Ensures score is strictly between 0 and 1, as required by validator.
    
    Parameters:
        total_reward (float): total reward accumulated by the agent
        steps (int): steps taken
        max_steps (int): maximum allowed steps

    Returns:
        float: score strictly in (0, 1)
    """
    # Basic score calculation
    score = total_reward / max_steps

    # Clip to ensure strictly between 0 and 1
    epsilon = 1e-5
    score = max(min(score, 1 - epsilon), 0 + epsilon)

    return score
