import os
import datetime
import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase() -> Client:
    # 1) Render / 실제 배포 환경 변수 우선
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    # 2) 로컬 개발 (secrets.toml)
    if not url:
        url = st.secrets.get("SUPABASE_URL", None)
    if not key:
        key = st.secrets.get("SUPABASE_KEY", None)

    if not url or not key:
        raise ValueError(
            "❗ SUPABASE_URL 또는 SUPABASE_KEY가 설정되지 않았습니다.\n"
            "Render에서는 환경 변수로 추가하고,\n"
            "로컬에서는 .streamlit/secrets.toml 사용하세요."
        )

    return create_client(url, key)


supabase = get_supabase()


# -------------------------
# AUTH
# -------------------------
def signup(email, password):
    if not email or not password:
        return None, "❌ 이메일과 비밀번호를 입력하세요."

    res = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    if res is None or res.user is None:
        return None, "❌ 회원가입 실패: 이미 존재하는 이메일이거나 유효하지 않습니다."

    return res.user, None


def login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        # User 객체만 반환 (중요)
        return res.user

    except Exception:
        return None


def logout():
    supabase.auth.sign_out()


def get_user():
    session = supabase.auth.get_session()
    if session and session.user:
        return session.user
    return None


# -------------------------
# HISTORY
# -------------------------
def save_history(user_id: str, problem: str, formula: str, explanation: str):
    data = {
        "user_id": user_id,
        "problem": problem,
        "formula": formula,
        "explanation": explanation,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    supabase.table("history").insert(data).execute()


def get_history(user_id: str):
    res = supabase.table("history") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .execute()

    return res.data

