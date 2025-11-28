import streamlit as st
from core.auth import login, signup, logout

st.title("⚡ 로그인")

# -----------------------
# 로그인 폼
# -----------------------
email = st.text_input("이메일")
pw = st.text_input("비밀번호", type="password")

if st.button("로그인"):
    result = login(email, pw)

    if result and result.user:
        st.session_state.user = result.user
        st.success("로그인 성공!")
        st.switch_page("pages/2_문제풀이.py")
    else:
        st.error("로그인 실패! 이메일/비밀번호를 확인하세요.")


# -----------------------
# 회원가입
# -----------------------
st.subheader("회원가입")

new_email = st.text_input("가입 이메일")
new_pw = st.text_input("가입 비밀번호", type="password")

if st.button("회원가입"):
    result = signup(new_email, new_pw)

    # result.user가 None이면 실패
    if result and result.user:
        st.success("회원가입 성공! 이메일 인증을 완료해주세요.")
    else:
        st.error("회원가입 실패! 이메일이 이미 존재하거나 유효하지 않습니다.")


# -----------------------
# 이미 로그인 상태라면 로그아웃 버튼 표시
# -----------------------
if "user" in st.session_state:
    st.info(f"현재 로그인: {st.session_state.user.email}")
    if st.button("로그아웃"):
        logout()
        st.success("로그아웃 완료!")
