from supabase import create_client
import os

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

supabase = create_client(url, key)

def fetch_one(table, column, value):
    res = supabase.table(table).select("*").eq(column, value).single().execute()
    if res.data:
        return res.data
    return None

def fetch_all(table):
    res = supabase.table(table).select("*").execute()
    return res.data

def insert(table, data: dict):
    res = supabase.table(table).insert(data).execute()
    return res.data
