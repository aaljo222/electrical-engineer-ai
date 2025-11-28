import streamlit as st
from core.history import get_history

if "user" not in st.session_state:
    st.switch_page("pages/1_로그인.py")

st.title("📜 나의 기록")

rows = get_history(st.session_state["user"]["id"])

for r in rows:
    st.markdown("### 문제")
    st.write(r["problem"])
    st.markdown("### 공식")
    st.write(r["formula"])
    st.markdown("### 설명")
    st.write(r["explanation"])
    st.divider()
