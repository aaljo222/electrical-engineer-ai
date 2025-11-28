import streamlit as st
import bcrypt
from core.db import supabase ,fetch_one, insert

def signup(email: str, password: str):
    exist = fetch_one("profiles", "email", email)
    if exist:
        return None, "이미 존재하는 이메일입니다."

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    insert("profiles", {
        "email": email,
        "password": hashed
    })

    return True, None


def login(email: str, password: str):
    user = fetch_one("profiles", "email", email)
    if not user:
        return None, "존재하지 않는 이메일입니다."

    hashed = user["password"].encode("utf-8")
    if not bcrypt.checkpw(password.encode("utf-8"), hashed):
        return None, "비밀번호가 일치하지 않습니다."

    return user, None


def check_login():
    user = get_user()
    if not user:
        st.switch_page("pages/1_로그인.py")
    return user



def get_user():
    if "user" not in st.session_state:
        return None
    return st.session_state["user"]


