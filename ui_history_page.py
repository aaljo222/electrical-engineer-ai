import streamlit as st
from auth_db import get_user, get_history

st.title("📝 내 학습 기록")

# 로그인 확인
user = get_user()
if not user:
    st.error("로그인이 필요합니다.")
    st.stop()

# 히스토리 가져오기 (res.data 아님!)
history = get_history(user.id)

if not history or len(history) == 0:
    st.info("아직 저장된 학습 기록이 없습니다.")
    st.stop()

# 히스토리 출력
for item in history:
    title = item["problem"][:40] + ("..." if len(item["problem"]) > 40 else "")
    with st.expander(f"📘 {title}"):
        st.write("### 📌 문제")
        st.write(item["problem"])

        st.write("### 🧮 공식")
        st.write(item["formula"])

        st.write("### 📖 설명")
        st.write(item["explanation"])

        st.write("---")
