# core/auth.py
import streamlit as st
from core.db import supabase
import bcrypt

def signup(email: str, password: str):
    exist = supabase.table("profiles").select("id").eq("email", email).single().execute()

    if exist.data:
        return False, "이미 존재하는 이메일입니다."

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    res = supabase.table("profiles").insert({
        "email": email,
        "password": hashed
    }).execute()

    return True, "회원가입 성공"

def login(email: str, password: str):
    row = supabase.table("profiles").select("*").eq("email", email).single().execute()

    if not row.data:
        return False, "이메일 없음"

    if not bcrypt.checkpw(password.encode(), row.data["password"].encode()):
        return False, "비밀번호 불일치"

    st.session_state["user"] = row.data
    return True, "로그인 성공"

def get_user():
    return st.session_state.get("user", None)

def check_login():
    user = get_user()
    if not user:
        st.error("로그인이 필요합니다.")
        st.stop()
    return user
