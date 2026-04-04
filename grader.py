def compute_score(total_reward, steps, max_steps):
    # normalize reward
    score = total_reward / max_steps

    # ensure score between 0 and 1
    if score < 0:
        score = 0

    if score > 1:
        score = 1

    return round(score, 2)