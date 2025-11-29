# core/history.py
from core.db import supabase

def save_history(user_id: str, problem: str, formula: str, explanation: str):
    supabase.table("history").insert({
    "user_id": user["id"],
    "problem": extracted_text,      # 문제 원문
    "formula": extracted_formula,   # Claude가 생성한 정답/공식
    "explanation": extracted_explanation  # Claude가 만든 풀이
}).execute()

def get_history(user_id: str):
    return (
        supabase.table("history")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
