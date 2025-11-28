from core.db import supabase
import streamlit as st

def signup(email: str, password: str):
    # 이메일 중복 여부 확인
    exist = supabase.table("profiles").select("*").eq("email", email).execute()

    if exist.data:
        return False, "이미 존재하는 이메일입니다."

    # DB insert
    supabase.table("profiles").insert({
        "email": email,
        "password": password
    }).execute()

    return True, None


def login(email: str, password: str):
    user = supabase.table("profiles")\
                   .select("*")\
                   .eq("email", email)\
                   .eq("password", password)\
                   .execute()

    if not user.data:
        return None, "이메일 또는 비밀번호가 잘못되었습니다."

    st.session_state["user"] = user.data[0]
    return user.data[0], None


def logout():
    if "user" in st.session_state:
        del st.session_state["user"]
