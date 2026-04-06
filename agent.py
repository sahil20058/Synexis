def choose_action(state):
    """
    state = {
        "agent_pos": [x, y],
        "victim_pos": [x, y],
        "steps": int
    }
    """

    ax, ay = state["agent_pos"]
    vx, vy = state["victim_pos"]

    # Move vertically first
    if ax < vx:
        return "DOWN"
    elif ax > vx:
        return "UP"

    # Then move horizontally
    if ay < vy:
        return "RIGHT"
    elif ay > vy:
        return "LEFT"

    # Already at victim (fallback)
    return "UP"