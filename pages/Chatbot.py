import streamlit as st
from core.ai_chat import answer_question
from core.auth import check_login

st.title("🤖 전기기사 AI 질문 챗봇")

user = check_login()

query = st.text_input("궁금한 내용을 입력하세요 (예: 변압기 등가회로, 콘덴서 역할 등)")

if st.button("질문하기"):
    with st.spinner("AI가 분석 중..."):
        answer = answer_question(query)

    st.markdown("### 💬 AI 답변")
    st.write(answer)
