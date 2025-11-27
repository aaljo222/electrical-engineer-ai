import streamlit as st
from auth_db import get_user, load_history


st.set_page_config(page_title="History")
user = get_user()

st.title("📜 내 학습 기록")

if not user:
    st.error("로그인 후 이용 가능합니다.")
    st.stop()

hist = load_history(user.user.id).data

for item in hist:
    st.markdown(
        f"""
        <div class='history-card'>
            <h4>{item['problem'][:40]}...</h4>
            <p><b>공식:</b> {item['formula']}</p>
            <details>
            <summary>결과 보기</summary>
            <p>{item['result']}</p>
            </details>
        </div>
        """,
        unsafe_allow_html=True
    )
