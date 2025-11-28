
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "core"))


import streamlit as st
from auth_db import get_user

st.title("⚡ My Profile")

user = get_user()

if not user:
    st.error("로그인이 필요합니다.")
    st.stop()

st.subheader("✉️ 이메일")
st.write(user.email)

st.subheader("🆔 User ID")
st.write(user.id)

if hasattr(user, "created_at"):
    st.subheader("📅 가입일")
    st.write(user.created_at)
