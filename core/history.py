from core.db import get_supabase

supabase = get_supabase()

def save_history(user_id, problem, formula, explanation):
    res = (
        supabase.table("user_history")
        .insert({
            "user_id": user_id,
            "problem": problem,
            "formula": formula,
            "explanation": explanation
        })
        .execute()
    )
    return res.data


def save_wrong_answer(user_id, problem_id):
    res = (
        supabase.table("user_wrongbook")
        .insert({
            "user_id": user_id,
            "problem_id": problem_id
        })
        .execute()
    )
    return res.data
