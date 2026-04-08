def get_task(task_name):
    if task_name == "easy":
        return {
            "grid_size": 5,
            "max_steps": 20
        }

    elif task_name == "medium":
        return {
            "grid_size": 7,
            "max_steps": 25
        }

    elif task_name == "hard":
        return {
            "grid_size": 10,
            "max_steps": 30
        }

    else:
        return {
            "grid_size": 5,
            "max_steps": 20
        }