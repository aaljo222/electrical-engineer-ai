import streamlit as st
from anthropic import Anthropic
import base64
import io
from PIL import Image
import os

from auth_db import login, signup, logout, save_history
from ui_history_page import render_history_page


# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="전기기사 공식 AI 설명 생성기",
    page_icon="⚡",
    layout="wide"
)

# CSS 적용
if os.path.exists("theme.css"):
    st.markdown("<style>" + open("theme.css").read() + "</style>", unsafe_allow_html=True)


# -------------------------
# ANTHROPIC CLIENT
# -------------------------
api_key = os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")

if not api_key:
    st.error("❗ Anthropic API Key가 없습니다. Streamlit Secrets에서 설정하세요.")
    st.stop()

client = Anthropic(api_key=api_key)


# -------------------------
# 이미지 OCR 함수
# -------------------------
def analyze_image(image_bytes):
    img_b64 = base64.b64encode(image_bytes).decode()

    prompt = """
전기기사 시험 문제 이미지입니다.

아래 JSON 형식으로 출력하세요:

{
 "problem": "...",
 "formula": "..."
}

JSON만 출력하세요. 설명 금지.
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1200,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": img_b64
                    }
                }
            ]
        }]
    )

    raw = response.content[0].text.strip()

    import json, re

    # 1) JSON 그대로 온 경우
    try:
        result = json.loads(raw)
        return result.get("problem", ""), result.get("formula", "")
    except:
        pass

    # 2) 텍스트 속 JSON 블록만 추출
    try:
        json_str = re.search(r"\{.*?\}", raw, re.S).group()
        result = json.loads(json_str)
        return result.get("problem", ""), result.get("formula", "")
    except:
        pass

    return "", ""


# -------------------------
# 설명 생성 함수
# -------------------------
def generate_explanation(problem, formula):
    prompt = f"""
전기기사 문제를 단계별로 설명하세요.

문제: {problem}
공식: {formula}

1) 문제 해석  
2) 필요한 개념  
3) 공식 해설  
4) 계산 예시  
5) 암기 팁  
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


# -------------------------
# 로그인 UI
# -------------------------
def login_ui():
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<div class='login-title'>⚡ 로그인</div>", unsafe_allow_html=True)

    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인", use_container_width=True):
        user = login(email, password)
        if user is None:
            st.error("❌ 로그인 실패! 이메일/비밀번호 확인하세요.")
        else:
            st.session_state.user = user
            st.success("로그인 완료!")
            st.experimental_rerun()

    st.markdown("---")
    st.subheader("회원가입")

    email2 = st.text_input("가입 이메일")
    password2 = st.text_input("가입 비밀번호", type="password")

    if st.button("회원가입", use_container_width=True):
        user, error = signup(email2, password2)
        if error:
            st.error(error)
        else:
            st.success("🎉 가입 완료!")

    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------
# 라우팅
# -------------------------
user = st.session_state.get("user")

if not user:
    login_ui()
    st.stop()

st.sidebar.success(f"로그인됨: {user['email']}")

# 기록 페이지 버튼
if st.sidebar.button("📜 내 기록 보기"):
    render_history_page(user["id"])
    st.stop()

if st.sidebar.button("로그아웃"):
    logout()
    st.session_state.pop("user", None)
    st.rerun()


# -------------------------
# 메인 UI
# -------------------------
st.title("⚡ 전기기사 공식 AI 설명 생성기")

uploaded = st.file_uploader("📸 문제 이미지 업로드", type=["png", "jpg", "jpeg"])

auto_problem = ""
auto_formula = ""

if uploaded:
    image = Image.open(uploaded)
    buf = io.BytesIO()
    image.convert("RGB").save(buf, format="JPEG")
    auto_problem, auto_formula = analyze_image(buf.getvalue())

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    problem_text = st.text_area("문제", auto_problem, height=150)
    formula_text = st.text_input("공식", auto_formula)

with col2:
    st.info("문제 입력 또는 이미지 업로드 후 '설명 생성하기' 클릭!")

st.divider()

# 설명 생성
if st.button("📖 설명 생성하기", type="primary"):
    if not problem_text.strip() or not formula_text.strip():
        st.error("문제와 공식을 입력하세요.")
    else:
        with st.spinner("AI가 설명을 생성 중입니다..."):
            explanation = generate_explanation(problem_text, formula_text)

        st.success("완료!")
        st.markdown(explanation)

        # 기록 저장
        save_history(user["id"], problem_text, formula_text, explanation)

        st.download_button(
            "📥 텍스트 다운로드",
            explanation,
            "explanation.txt"
        )
