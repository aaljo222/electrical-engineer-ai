from core.db import execute, fetch_all


def save_history(user_id, problem, formula, explanation):
    execute(
        "INSERT INTO history (user_id, problem, formula, explanation) VALUES (%s, %s, %s, %s)",
        (user_id, problem, formula, explanation)
    )


def get_history(user_id):
    return fetch_all(
        "SELECT * FROM history WHERE user_id=%s ORDER BY id DESC",
        (user_id,)
    )
