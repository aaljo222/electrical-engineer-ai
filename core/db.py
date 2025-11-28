import os
from supabase import create_client

def init_supabase():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise Exception("❌ SUPABASE_URL or SUPABASE_KEY missing in Streamlit Secrets!")

    return create_client(url, key)
