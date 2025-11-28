import streamlit as st
from core.auth import get_user
from core.history import get_history

st.title("📘 내 학습 기록")

user = get_user()
if not user:
    st.warning("로그인이 필요합니다.")
    st.stop()

history = get_history(user["id"])

st.table(history)
