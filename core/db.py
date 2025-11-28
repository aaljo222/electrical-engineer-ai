import os
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# supabase 클라이언트 생성 (전역)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# supabase 클라이언트 생성 (전역)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_resource
def get_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("❗ SUPABASE 설정이 없습니다.")

    return create_client(url, key)


# 하나의 row 가져오기
def fetch_one(table: str, column: str, value):
    supabase = get_supabase()

    res = (
        supabase.table(table)
        .select("*")
        .eq(column, value)
        .limit(1)
        .execute()
    )

    if not res.data:
        return None

    return res.data[0]


# 여러 row 가져오기
def fetch_all(table: str, filters: dict = None):
    supabase = get_supabase()

    query = supabase.table(table).select("*")

    if filters:
        for col, val in filters.items():
            query = query.eq(col, val)

    res = query.execute()
    return res.data or []


# row 삽입
def insert(table: str, data: dict):
    supabase = get_supabase()
    res = supabase.table(table).insert(data).execute()
    return res.data
