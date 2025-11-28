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
        st.session_state["user"] = user
        st.success("로그인 성공!")

# 로그인 후 다른 페이지로 자동 이동
if "user" in st.session_state:
    st.switch_page("pages/Dashboard.py")



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

def check_login():
    # 로그인 안 되어 있으면 로그인 페이지로 이동
    user = st.session_state.get("user")
    if not user:
        st.error("로그인이 필요합니다.")
        st.stop()

    return user