import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("🚨 환경변수에 SUPABASE_URL / SUPABASE_KEY 가 없습니다.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
