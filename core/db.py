import os
from supabase import create_client, Client
# Supabase 클라이언트 생성
def get_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("🚨 SUPABASE_URL 또는 SUPABASE_KEY 환경변수가 없습니다!")

    return create_client(url, key)


# 1) 단일 row 조회
supabase = get_supabase()

def fetch_one(table: str, column: str, value):
    res = supabase.table(table).select("*").eq(column, value).maybe_single().execute()
    return res.data  # data는 None일 수 있음 → 문제 없음



# 2) 전체 조회
def fetch_all(table: str):
    res = supabase.table(table).select("*").execute()
    return res.data

# 3) INSERT
def insert(table: str, data: dict):
    res = supabase.table(table).insert(data).execute()
    return res.data
