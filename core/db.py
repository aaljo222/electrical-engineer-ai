import os
from supabase import create_client, Client
import streamlit as st


@st.cache_resource
def get_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("❗ SUPABASE 설정이 없습니다. 환경변수 또는 secrets.toml 확인하세요.")

    return create_client(url, key)


def fetch_one(table: str, column: str, value):
    supabase = get_supabase()
    res = supabase.table(table).select("*").eq(column, value).maybe_single()

    # row가 없을 경우 None 반환 (중요!)
    if res is None or res.data is None:
        return None

    return res.data


def insert(table: str, row: dict):
    supabase = get_supabase()
    res = supabase.table(table).insert(row).execute()
    return res.data
