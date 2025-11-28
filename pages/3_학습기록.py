import streamlit as st
from core.auth import require_login
from core.history import load_history

require_login()

st.title("📜 학습 기록")

hist = load_history(st.session_state.user["id"])

for h in hist:
    st.write("### ✏ 문제")
    st.write(h["problem"])

    st.write("### 📐 공식")
    st.write(h["formula"])

    st.write("### 📘 설명")
    st.write(h["explanation"])

    st.divider()
