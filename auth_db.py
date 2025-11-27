import streamlit as st
from supabase import create_client, Client   # ✔ 올바른 형태
import json
import datetime


@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase()

# -------------- AUTH --------------
def signup(email, password):
    # 빈값 체크
    if not email or not password:
        return None, "❌ 이메일과 비밀번호를 입력하세요."

    res = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    # Supabase 에러 체크
    if res is None or res.user is None:
        return None, "❌ 회원가입 실패: 이미 존재하는 이메일이거나 유효하지 않습니다."

    return res.user, None


def login(email, password):
    try:
        result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return result.user
    except Exception:
        return None

def logout():
    supabase.auth.sign_out()

def get_user():
    session = supabase.auth.get_session()
    if session is None or session.user is None:
        return None
    return session.user


# -------------- HISTORY DB --------------
def save_history(user_id: str, problem_text: str, formula: str, explanation: str):
    data = {
        "user_id": user_id,
        "problem": problem_text,
        "formula": formula,
        "explanation": explanation,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    supabase.table("history").insert(data).execute()


def get_history(user_id):
    res = supabase.table("history").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return res.data


def load_history(user_id):
    return supabase.table("history").select("*").eq("user_id", user_id).order("id", desc=True).execute()
