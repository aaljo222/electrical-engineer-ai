import hashlib
import streamlit as st
from core.db import select, insert

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def signup(email, password):
    existing = select("users", {"email": f"eq.{email}"})
    if existing:
        return None, "이미 존재하는 이메일입니다."

    h = hash_pw(password)
    user = insert("users", {"email": email, "password": h})
    return user, None

def login(email, password):
    h = hash_pw(password)
    user = select("users", {"email": f"eq.{email}", "password": f"eq.{h}"})
    return user[0] if user else None

def require_login():
    if "user" not in st.session_state:
        st.switch_page("pages/1_로그인.py")
