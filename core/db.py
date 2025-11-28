# core/db.py
import os
from supabase import create_client, Client

def get_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("🚨 SUPABASE_URL 또는 SUPABASE_KEY 환경변수가 없습니다!")

    return create_client(url, key)


def fetch_all(table: str):
    supabase = get_supabase()
    res = supabase.table(table).select("*").execute()
    return res.data


def fetch_one(table: str, column: str, value):
    supabase = get_supabase()
    res = supabase.table(table).select("*").eq(column, value).maybe_single().execute()
    return res.data   # data는 None 가능 → 문제 없음


def insert(table: str, row: dict):
    supabase = get_supabase()
    res = supabase.table(table).insert(row).execute()
    return res.data
