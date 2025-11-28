# supabase_rest.py
import os
import requests
import json

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def _rest_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

def db_select(table, filters=None, limit=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = _rest_headers()

    params = {}
    if filters:
        params.update(filters)
    if limit:
        params["limit"] = limit

    res = requests.get(url, headers=headers, params=params)
    if res.status_code >= 400:
        print("[SELECT ERROR]", res.text)
        return []
    return res.json()

def db_insert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = _rest_headers()
    headers["Prefer"] = "return=representation"

    res = requests.post(url, headers=headers, data=json.dumps(data))
    if res.status_code >= 400:
        print("[INSERT ERROR]", res.text)
        return None
    return res.json()

def db_update(table, filters, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = _rest_headers()

    params = filters

    res = requests.patch(url, headers=headers, params=params, data=json.dumps(data))
    if res.status_code >= 400:
        print("[UPDATE ERROR]", res.text)
        return None
    return res.json()

def db_delete(table, filters):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = _rest_headers()

    res = requests.delete(url, headers=headers, params=filters)
    return res.status_code
