import requests
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

def supabase_query(sql, params=()):
    payload = {
        "query": sql,
        "params": params,
    }
    url = f"{SUPABASE_URL}/rest/v1/rpc/pg_rpc"
    res = requests.post(url, json=payload, headers=headers)
    return res.json()
