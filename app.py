
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "core"))


import streamlit as st
from core.auth import check_login, logout
from core.db import init_supabase

st.set_page_config(page_title="전기기사 AI 학습 플랫폼", page_icon="⚡", layout="wide")

supabase = init_supabase()

user = check_login()
if user:
    st.sidebar.success(f"{user.email} 님 환영합니다!")

    if st.sidebar.button("로그아웃"):
        logout()
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/1_문제_풀이.py", label="📘 문제 풀이")
    st.sidebar.page_link("pages/2_오답노트.py", label="📕 오답노트")
    st.sidebar.page_link("pages/3_추천문제.py", label="🎯 추천 문제")
    st.sidebar.page_link("pages/4_프로필.py", label="👤 프로필")
else:
    st.switch_page("pages/login.py")
