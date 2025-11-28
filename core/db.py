# core/db.py
import os
from supabase import create_client


def init_supabase():
    """
    Streamlit Cloud에서 환경변수가 늦게 로드되는 문제를 방지하기 위해
    호출 시점마다 Supabase 객체를 새로 생성하는 구조.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise Exception("🚨 SUPABASE_URL 또는 SUPABASE_KEY 환경변수가 없습니다.")

    return create_client(url, key)


# 전역 사용 가능 객체 (선택적)
supabase = init_supabase()
