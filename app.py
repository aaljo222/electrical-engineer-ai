import streamlit as st

st.set_page_config(page_title="Electrical Engineer AI", layout="wide")

# 로그인 상태 표시
if "user" in st.session_state:
    st.sidebar.success(f"로그인됨: {st.session_state['user']['email']}")
else:
    st.sidebar.warning("로그인 필요")

st.title("Electrical Engineer AI 메인 페이지")
st.write("왼쪽 메뉴에서 기능을 선택하세요.")
