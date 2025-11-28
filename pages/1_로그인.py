import streamlit as st
from core.auth import signup, login

st.title("⚡ 로그인")

# 로그인 폼
email = st.text_input("이메일")
pw = st.text_input("비밀번호", type="password")

if st.button("로그인"):
    user = login(email, pw)
    if user:
        st.session_state.user = user
        st.success("로그인 성공!")
    else:
        st.error("로그인 실패!")

st.subheader("회원가입")
reg_email = st.text_input("가입 이메일")
reg_pw = st.text_input("가입 비밀번호", type="password")

if st.button("회원가입"):
    ok, err = signup(reg_email, reg_pw)
    if ok:
        st.success("회원가입 성공!")
    else:
        st.error(err)
