from supabase import create_client
from datetime import datetime
import os

# Supabase 연결
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


from core.db import supabase

def save_history(user_id, problem_id, user_answer, explanation, is_correct):
    """유저 풀이 기록 저장"""
    supabase.table("user_history").insert({
        "user_id": user_id,
        "problem_id": problem_id,
        "user_answer": user_answer,
        "is_correct": is_correct,
        "explanation": explanation
    }).execute()


def load_history(user_id):
    """특정 사용자의 풀이 기록 불러오기"""
    try:
        result = (
            supabase.table("history")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        return result.data

    except Exception as e:
        print("❌ [history 불러오기 오류]", str(e))
        return []
