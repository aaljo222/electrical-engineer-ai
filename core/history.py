from core.db import execute, fetch_all


from core.db import insert

def save_history(user_id, problem, formula, explanation):
    data = {
        "user_id": user_id,
        "problem": problem,
        "formula": formula,
        "explanation": explanation
    }
    insert("history", data)



def get_history(user_id):
    return fetch_all(
        "SELECT * FROM history WHERE user_id=%s ORDER BY id DESC",
        (user_id,)
    )
