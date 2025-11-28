# ui_history_page.py
import streamlit as st
from auth_db import get_history

def render_history_page(user_id):
    st.title("📝 내 학습 기록")

    history = get_history(user_id)

    if not history:
        st.info("기록이 없습니다.")
        return

    for item in sorted(history, key=lambda x: x["created_at"], reverse=True):
        with st.expander(item["problem"][:50]):
            st.subheader("📘 문제")
            st.write(item["problem"])

            st.subheader("📐 공식")
            st.write(item["formula"])

            st.subheader("🧠 설명")
            st.write(item["explanation"])

            st.caption(f"작성일: {item['created_at']}")
