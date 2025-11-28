import streamlit as st
from core.auth import signup, login


st.title("⚡ 로그인 / 회원가입")

st.subheader("로그인")

email = st.text_input("이메일")
pw = st.text_input("비밀번호", type="password")

if st.button("로그인"):
    user, err = login(email, pw)

    if err:
        st.error(err)
    else:
        st.success("로그인 성공!")
        st.session_state["user"] = user
        st.rerun()


st.write("---")
st.subheader("회원가입")

reg_email = st.text_input("가입 이메일")
reg_pw = st.text_input("가입 비밀번호", type="password")

if st.button("회원가입"):
    ok, err = signup(reg_email, reg_pw)
    if ok:
        st.success("회원가입 완료!")
    else:
        st.error(err)
