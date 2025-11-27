import streamlit as st
from supabase import create_client, Client   # ✔ 올바른 형태
import json
import datetime


import os
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase() -> Client:
    # 1) Render/Production 환경 변수 우선
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    # 2) 로컬 개발(Streamlit secrets) 지원
    if not url:
        url = st.secrets.get("SUPABASE_URL", None)
    if not key:
        key = st.secrets.get("SUPABASE_KEY", None)

    # 3) 그래도 없으면 명확한 에러
    if not url or not key:
        raise ValueError(
            "❗ SUPABASE_URL 또는 SUPABASE_KEY가 설정되지 않았습니다.\n"
            "Render에서는 환경변수로 추가하고,\n"
            "로컬에서는 .streamlit/secrets.toml을 사용하세요."
        )

    return create_client(url, key)

supabase = get_supabase()

# -------------- AUTH --------------
def signup(email, password):
    # 빈값 체크
    if not email or not password:
        return None, "❌ 이메일과 비밀번호를 입력하세요."

    res = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    # Supabase 에러 체크
    if res is None or res.user is None:
        return None, "❌ 회원가입 실패: 이미 존재하는 이메일이거나 유효하지 않습니다."

    return res.user, None


def login_ui():
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<div class='login-title'>⚡ 로그인</div>", unsafe_allow_html=True)

    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")

    # 로그인 버튼
    if st.button("로그인", use_container_width=True):
        user_obj = login(email, password)

        if user_obj is None:
            st.error("❌ 로그인 실패! 이메일/비밀번호를 확인하세요.")
            return

        st.success("✔ 로그인 성공!")
        st.session_state.user = user_obj
        st.experimental_rerun()

    st.markdown("----")
    st.subheader("회원가입")

    email2 = st.text_input("가입 이메일")
    password2 = st.text_input("가입 비밀번호", type="password")

    if st.button("회원가입", use_container_width=True):
        user, error = signup(email2, password2)

        if error:
            st.error(error)
        else:
            st.success("🎉 가입 완료! 이메일 인증을 완료하세요.")

    st.markdown("</div>", unsafe_allow_html=True)


def logout():
    supabase.auth.sign_out()

def get_user():
    session = supabase.auth.get_session()
    if session is None or session.user is None:
        return None
    return session.user


# -------------- HISTORY DB --------------
def save_history(user_id: str, problem_text: str, formula: str, explanation: str):
    data = {
        "user_id": user_id,
        "problem_text": problem_text,
        "formula": formula,
        "explanation": explanation,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    supabase.table("user_history").insert(data).execute()


def get_history(user_id):
    res = supabase.table("user_history") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .execute()
    return res.data



def load_history(user_id):
    return supabase.table("history").select("*").eq("user_id", user_id).order("id", desc=True).execute()
