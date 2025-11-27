import streamlit as st
import anthropic
import hashlib
import base64
import io
from PIL import Image
from auth_db import login, signup, get_user, logout, save_history, get_history



# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="전기기사 공식 AI 설명 생성기", page_icon="⚡", layout="wide")
st.markdown("<style>" + open("theme.css").read() + "</style>", unsafe_allow_html=True)

# -------------------------
# API
# -------------------------
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])


# -------------------------
# IMAGE → OCR
# -------------------------
def analyze_image(image_bytes):
    img_b64 = base64.b64encode(image_bytes).decode()

    prompt = """
전기기사 시험 문제 이미지입니다.
아래 JSON 형식으로 문제만 추출하세요:

{
 "problem": "...",
 "formula": "..."
}
"""

    message = client.messages.create(
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

    import json
    result = json.loads(message.content[0].text)
    return result.get("problem", ""), result.get("formula", "")


# -------------------------
# Explain
# -------------------------
def generate_explanation(problem, formula):
    prompt = f"""
전기기사 문제를 단계별로 설명하세요.

문제: {problem}
공식: {formula}

1. 문제 이해  
2. 필요한 개념  
3. 공식 유도  
4. 예제 풀이  
5. 암기 팁  
"""

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


# -------------------------
# AUTH UI
# -------------------------
def login_ui():
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<div class='login-title'>⚡ 로그인</div>", unsafe_allow_html=True)

    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인", use_container_width=True):
        res = login(email, password)

        # 로그인 실패 처리
        if res is None or res.user is None:
            st.error("❌ 로그인 실패! 이메일 또는 비밀번호를 확인하세요.")
            return

        # 로그인 성공 처리
        st.success("✔ 로그인 성공!")
        st.session_state.user = res.user   # 세션에 저장
        st.experimental_rerun()


    st.markdown("----")
    st.subheader("회원가입")

    email2 = st.text_input("가입 이메일")
    password2 = st.text_input("가입 비밀번호", type="password")

    if st.button("회원가입", use_container_width=True):
        res = signup(email2, password2)
        st.success("가입 완료!")

    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------
# MAIN APP
# -------------------------
user = get_user()

if not user:
    login_ui()
    st.stop()

st.sidebar.success(f"로그인됨: {user.user.email}")
if st.sidebar.button("로그아웃"):
    logout()
    st.experimental_rerun()


# =============== Main App UI ===============
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
    st.subheader("📝 문제 입력")
    problem_text = st.text_area("문제", auto_problem, height=150)
    formula_text = st.text_input("공식", auto_formula)

with col2:
    st.info("문제 업로드 또는 입력 후 생성 버튼을 누르세요.")

st.divider()

if st.button("📖 설명 생성하기", type="primary"):
    if problem_text.strip() == "" or formula_text.strip() == "":
        st.error("문제/공식을 입력하세요.")
    else:
        with st.spinner("AI가 설명을 생성 중입니다..."):
            explanation = generate_explanation(problem_text, formula_text)

        st.success("완료!")
        st.markdown(explanation)

        save_history(user.user.id, problem_text, formula_text, explanation)

        st.download_button(
            "📥 텍스트 다운로드",
            data=explanation,
            file_name="explanation.txt"
        )
