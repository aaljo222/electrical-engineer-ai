import streamlit as st
from core.db import supabase
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def check_login():
    if "user" not in st.session_state:
        st.session_state["user"] = None

    if st.session_state["user"]:
        return True

    st.subheader("로그인")
    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        hashed = hash_password(password)

        user = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .eq("password", hashed)
            .execute()
        )

        if user.data:
            st.session_state["user"] = user.data[0]
            st.success("로그인 성공!")
            st.experimental_rerun()
        else:
            st.error("이메일 또는 비밀번호가 틀렸습니다.")

    return False


def logout():
    st.session_state["user"] = None
    st.experimental_rerun()
