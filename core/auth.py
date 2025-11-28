# core/auth.py
import streamlit as st
from core.db import supabase

# Streamlit session key
USER_SESSION_KEY = "logged_user"


def check_login():
    """
    Streamlit 세션에 로그인 정보가 있는지 확인
    """
    if USER_SESSION_KEY in st.session_state:
        return st.session_state[USER_SESSION_KEY]
    return None


def login(email, password):
    """
    Supabase Auth 테이블 기준 로그인 처리
    """
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

        return False

    except Exception as e:
        st.error(f"로그인 실패: {e}")
        return False


def logout():
    """
    로그아웃 → 세션 제거
    """
    if USER_SESSION_KEY in st.session_state:
        del st.session_state[USER_SESSION_KEY]
    st.success("로그아웃 되었습니다.")


def login_form():
    """
    로그인 화면 UI 템플릿
    """
    st.subheader("🔐 로그인")

    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인", use_container_width=True):
        if login(email, password):
            st.success("로그인 성공!")
            st.rerun()
