import requests
import streamlit as st
import os

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

def select(table, eq=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    params = {"select": "*"}

    if eq:
        params.update(eq)

    res = requests.get(url, headers=headers, params=params)
    return res.json()

def insert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    res = requests.post(url, headers=headers, json=data)
    return res.json()

def update(table, match, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    res = requests.patch(url, headers=headers, params=match, json=data)
    return res.json()
