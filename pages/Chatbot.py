import streamlit as st
from core.auth import check_login
from core.ai_chat import ask_ai

st.title("💬 전기기사 AI 질문답변")

check_login()

question = st.text_input("질문 입력")

if st.button("질문 보내기"):
    st.write(ask_ai(question))
