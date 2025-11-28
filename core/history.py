from core.db import get_supabase

supabase = get_supabase()

def save_history(user_id, problem, formula, explanation):
    return supabase.table("user_history").insert({
        "user_id": user_id,
        "problem": problem,
        "formula": formula,
        "explanation": explanation
    }).execute().data


def save_wrong_answer(user_id, problem_id):
    return supabase.table("user_wrongbook").insert({
        "user_id": user_id,
        "problem_id": problem_id
    }).execute().data
