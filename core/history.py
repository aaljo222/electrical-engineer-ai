from supabase import create_client
from datetime import datetime
import os

# Supabase 연결
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_history(user_id, problem, formula, explanation):
    """문제 풀이 기록을 history 테이블에 저장"""

    try:
        data = {
            "user_id": user_id,        # uuid 그대로 저장
            "problem": problem,
            "formula": formula,
            "explanation": explanation,
            "created_at": datetime.utcnow().isoformat()
        }

        result = supabase.table("history").insert(data).execute()
        return result.data

    except Exception as e:
        print("❌ [history 저장 오류]", str(e))
        return None


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
