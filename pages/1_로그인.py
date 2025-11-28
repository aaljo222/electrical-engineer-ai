import streamlit as st
from core.auth import login, signup


st.title("⚡ 로그인")

email = st.text_input("이메일")
pw = st.text_input("비밀번호", type="password")

if st.button("로그인"):
    user = login(email, pw)
    if user:
        st.session_state.user = user
        st.success("로그인 성공!")
        st.switch_page("pages/2_문제풀이.py")
    else:
        st.error("로그인 실패")

st.divider()
st.subheader("회원가입")

email2 = st.text_input("가입 이메일")
pw2 = st.text_input("가입 비밀번호", type="password")

if st.button("회원가입"):
    user, err = signup(email2, pw2)
    if err:
        st.error(err)
    else:
        st.success("회원가입 완료!")
