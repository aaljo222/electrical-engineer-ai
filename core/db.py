# core/db.py
import os
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("❌ Supabase 환경변수 누락")

    return create_client(url, key)

supabase = get_supabase()
