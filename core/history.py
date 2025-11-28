from core.db import insert, select

def save_history(user_id, problem, formula, explanation):
    insert(
        "history",
        {
            "user_id": user_id,
            "problem": problem,
            "formula": formula,
            "explanation": explanation,
        }
    )

def load_history(user_id):
    return select("history", {"user_id": f"eq.{user_id}"})
