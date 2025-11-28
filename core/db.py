# core/db.py
import os
from supabase import create_client

def init_supabase():
    """
    Streamlit Cloud 에서 환경변수가 늦게 로드되는 문제를 방지하기 위해
    함수 호출 시점에 Supabase 객체를 생성하는 구조.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise Exception("🚨 SUPABASE_URL 또는 SUPABASE_KEY가 환경변수에 없습니다.")

    return create_client(url, key)


# 전역 사용 가능
supabase = init_supabase()
