from core.db import supabase
import streamlit as st


# ---------------------------
# 회원가입 (공식 방식)
# ---------------------------
def signup(email: str, password: str):
    try:
        result = supabase.auth.sign_up(
            {"email": email, "password": password}
        )
        return result
    except Exception as e:
        return None


# ---------------------------
# 로그인 (공식 방식)
# ---------------------------
def login(email: str, password: str):
    try:
        result = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        return result
    except Exception:
        return None


# ---------------------------
# 로그아웃
# ---------------------------
def logout():
    supabase.auth.sign_out()
    st.session_state.pop("user", None)


# ---------------------------
# 로그인 요구 데코레이터
# ---------------------------
def require_login():
    if "user" not in st.session_state:
        st.warning("로그인이 필요합니다.")
        st.stop()
