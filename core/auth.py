import streamlit as st
from supabase import create_client
import os

# --------------------------------------
# SUPABASE CLIENT
# --------------------------------------
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# --------------------------------------
# 로그인 체크
# --------------------------------------
def check_login():
    """
    로그인 안되어 있으면 login 페이지로 강제 이동
    """
    if "user" not in st.session_state or st.session_state["user"] is None:
        st.switch_page("Profile.py")  # 로그인 페이지 이름에 맞게 수정
        st.stop()
    return st.session_state["user"]


# --------------------------------------
# 로그인 함수
# --------------------------------------
def login(email: str, password: str):
    try:
        result = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )

        if result.user:
            st.session_state["user"] = result.user
            return True, "로그인 성공"

        return False, "로그인 실패"

    except Exception as e:
        return False, f"로그인 오류: {e}"


# --------------------------------------
# 로그아웃
# --------------------------------------
def logout():
    try:
        supabase.auth.sign_out()
    except:
        pass

    st.session_state["user"] = None
    st.switch_page("Profile.py")   # 로그인 페이지로 이동
