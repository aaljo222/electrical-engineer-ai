import os
from supabase import create_client
import streamlit as st

# --------------------------------------
# Supabase 초기화
# --------------------------------------
def init_supabase():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        st.error("❗ Supabase 환경변수가 설정되지 않았습니다.")
        st.stop()

    return create_client(url, key)


# 글로벌 supabase client
supabase = init_supabase()


# --------------------------------------
# 공통 함수: 레코드 가져오기
# --------------------------------------
def fetch_all(table: str):
    return supabase.table(table).select("*").execute().data


# --------------------------------------
# 공통 함수: insert
# --------------------------------------
def insert(table: str, data: dict):
    return supabase.table(table).insert(data).execute()
