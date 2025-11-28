from core.db import supabase

def save_history(user_id: str, problem: str, formula: str, explanation: str):
    supabase.table("history").insert({
        "user_id": user_id,
        "problem": problem,
        "formula": formula,
        "explanation": explanation
    }).execute()

def get_history(user_id: str):
    res = supabase.table("history").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return res.data
