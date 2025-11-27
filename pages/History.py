import streamlit as st
from auth_db import get_user, get_history

st.title("📝 내 학습 기록")

# 로그인 확인
user = get_user()
if not user:
    st.error("로그인이 필요합니다.")
    st.stop()

# 히스토리 불러오기
history = get_history(user.id)   # ← .data 절대 붙이지 말 것

if not history:
    st.info("아직 저장된 학습 기록이 없습니다.")
    st.stop()

# 히스토리 표시
for item in history:
    with st.expander(f"📘 {item['problem'][:30]}..."):
        st.write("### 📌 문제")
        st.write(item["problem"])

        st.write("### 🧮 공식")
        st.write(item["formula"])

        st.write("### 📖 설명")
        st.write(item["result"])

        st.write("—")
