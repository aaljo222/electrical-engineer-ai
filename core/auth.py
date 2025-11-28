import streamlit as st
import bcrypt
from core.db import supabase

# 회원가입
def signup(email: str, password: str):
    # 이미 존재하는 이메일인지 확인
    exist = supabase.table("profiles").select("*").eq("email", email).execute()
    if exist.data:
        return False, "이미 가입된 이메일입니다."

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    result = supabase.table("profiles").insert({
        "email": email,
        "password": hashed
    }).execute()

    return True, "회원가입 완료!"

# 로그인
def login(email: str, password: str):
    user = supabase.table("profiles").select("*").eq("email", email).single().execute()

    if not user.data:
        return False, "가입되지 않은 이메일입니다."

    hashed = user.data["password"]

    if not bcrypt.checkpw(password.encode(), hashed.encode()):
        return False, "비밀번호가 틀렸습니다."

    # 로그인 성공 → 세션 저장
    st.session_state["user"] = user.data
    return True, "로그인 성공!"

# 현재 로그인 유저 가져오기
def get_user():
    return st.session_state.get("user")

# 로그인 안 되어 있으면 로그인 페이지로 이동
def check_login():
    if "user" not in st.session_state:
        st.switch_page("pages/1_로그인.py")
    return st.session_state["user"]
