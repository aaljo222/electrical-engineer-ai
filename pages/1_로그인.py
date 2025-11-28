import streamlit as st
from core.auth import signup, login, logout

st.title("⚡ 로그인")

# ---------- 로그인 ----------
email = st.text_input("이메일")
pw = st.text_input("비밀번호", type="password")

if st.button("로그인"):
    user, err = login(email, pw)
    if err:
        st.error(err)
    else:
        st.session_state["user"] = user
        st.success(f"{user['email']} 님 환영합니다!")

# ---------- 회원가입 ----------
st.subheader("회원가입")

reg_email = st.text_input("가입 이메일")
reg_pw = st.text_input("가입 비밀번호", type="password")

if st.button("회원가입"):
    ok, err = signup(reg_email, reg_pw)
    if err:
        st.error(err)
    else:
        st.success("회원가입 성공!")

# ---------- 로그아웃 ----------
if "user" in st.session_state:
    st.write(f"현재 로그인: {st.session_state['user']['email']}")
    if st.button("로그아웃"):
        logout()
        st.session_state.clear()
        st.success("로그아웃 완료")
