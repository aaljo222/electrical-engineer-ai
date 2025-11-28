from supabase import create_client
import os

# Supabase 클라이언트 생성
def get_client():
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_client()

# 1) 단일 row 조회
def fetch_one(table: str, column: str, value):
    res = supabase.table(table).select("*").eq(column, value).maybe_single().execute()
    return res.data


# 2) 전체 조회
def fetch_all(table: str):
    res = supabase.table(table).select("*").execute()
    return res.data

# 3) INSERT
def insert(table: str, data: dict):
    res = supabase.table(table).insert(data).execute()
    return res.data
