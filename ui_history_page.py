import streamlit as st
from auth_db import get_history

def render_history_page(user_id):

    st.title("📜 내가 생성한 설명 기록")

    history = get_history(user_id)

    if not history:
        st.info("아직 생성된 설명 기록이 없습니다.")
        if st.button("돌아가기"):
            st.session_state.page = "main"
            st.experimental_rerun()
        return

    for item in history:
        with st.expander(f"📝 문제: {item['problem'][:30]}..."):
            st.markdown(f"**📘 문제:**\n\n{item['problem']}")
            st.markdown(f"**🧮 공식:**\n\n{item['formula']}")
            st.markdown(f"**📖 설명:**\n\n{item['explanation']}")
            st.markdown(f"**⏱ 생성일:** {item['created_at']}")

    st.divider()

    if st.button("⬅ 돌아가기"):
        st.session_state.page = "main"
        st.experimental_rerun()
