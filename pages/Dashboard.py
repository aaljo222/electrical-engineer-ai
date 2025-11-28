import streamlit as st
from core.auth import get_user
from core.history import get_history

user = get_user()

if not user:
    st.warning("로그인이 필요합니다.")
    st.stop()

st.title("📊 사용자 학습 대시보드")

history = get_history(user["id"])

st.write("### 최근 학습 기록")
st.table(history[:10])
