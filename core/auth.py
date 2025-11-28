# core/auth.py
import streamlit as st
from core.db import init_supabase

# 세션 저장 키
USER_SESSION_KEY = "logged_user"


def check_login():
    """Streamlit 세션에 로그인 정보가 있는지 확인"""
    if USER_SESSION_KEY in st.session_state:
        return st.session_state[USER_SESSION_KEY]
    return None


def login(email, password):
    """Supabase Auth 로그인 처리"""
    supabase = init_supabase()
    try:
        result = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        user = result.user

        if user:
            st.session_state[USER_SESSION_KEY] = {
                "email": user.email,
                "id": user.id,
            }
            return True

    except Exception as e:
        st.error(f"로그인 실패: {e}")

    return False


def logout():
    """로그아웃"""
    if USER_SESSION_KEY in st.session_state:
        del st.session_state[USER_SESSION_KEY]


def require_login():
    """로그인이 필요한 페이지 보호"""
    user = check_login()
    if not user:
        st.error("로그인이 필요합니다.")
        st.stop()

    return user
