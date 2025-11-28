import streamlit as st
from core.auth import check_login
from core.explain import generate_concept_summary

st.title("📚 AI 기반 개념 정리 생성기")

user = check_login()

topic = st.text_input("정리할 개념을 입력하세요 (예: 유전율, 페이저, 단상전력, 변압기 등)")

if st.button("개념 정리 생성"):
    with st.spinner("AI가 개념을 학습하고 정리 중입니다..."):
        summary = generate_concept_summary(topic)

    st.markdown("### 📘 개념 정리")
    st.write(summary)
