import streamlit as st
from auth_db import get_user, load_history

st.title("⚡ My Profile")

user = get_user()
if not user:
    st.error("로그인 필요")
else:
    st.write("### 이메일")
    st.write(user.user.email)

    st.write("### User ID")
    st.write(user.user.id)
