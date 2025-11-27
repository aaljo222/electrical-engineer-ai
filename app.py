import streamlit as st
import anthropic
import hashlib
import os
import re
import base64
import io
from PIL import Image
from supabase import create_client, Client
from datetime import datetime, timedelta

# ===========================================
# 기본 설정
# ===========================================
st.set_page_config(page_title="전기기사 공식 AI", page_icon="⚡", layout="wide")

# -------------------------------------------
# Supabase 설정
# -------------------------------------------
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")  # 반드시 anon key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

if "user" not in st.session_state:
    st.session_state.user = None


# ===========================================
# 로그인 UI
# ===========================================
def login_ui():
    st.subheader("🔐 로그인")

    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        try:
            data = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = data.user
            st.success("로그인 성공!")
            st.experimental_rerun()
        except Exception as e:
            st.error("로그인 실패: 이메일 또는 비밀번호 확인")


def signup_ui():
    st.subheader("📝 회원가입")

    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")

    if st.button("회원가입"):
        try:
            supabase.auth.sign_up({"email": email, "password": password})
            st.success("회원가입 성공! 이메일을 확인하세요.")
        except Exception as e:
            st.error(f"회원가입 실패: {e}")


# ===========================================
# 회원 정보 / 사용량 처리
# ===========================================
MAX_DAILY = 5  # 하루 사용 제한

def get_usage(user_id):
    res = supabase.table("usage").select("*").eq("user_id", user_id).execute()

    if len(res.data) == 0:
        # 신규 유저 → 레코드 생성
        supabase.table("usage").insert({
            "user_id": user_id,
            "count": 0,
            "updated_at": datetime.now().isoformat()
        }).execute()
        return 0

    record = res.data[0]

    # 날짜 변경되면 초기화
    last = datetime.fromisoformat(record["updated_at"])
    if (datetime.now() - last).days >= 1:
        supabase.table("usage").update({"count": 0, "updated_at": datetime.now().isoformat()}).eq("user_id", user_id).execute()
        return 0

    return record["count"]


def increment_usage(user_id):
    supabase.table("usage").update({
        "count": supabase.table("usage").select("count").eq("user_id", user_id).execute().data[0]["count"] + 1,
        "updated_at": datetime.now().isoformat()
    }).eq("user_id", user_id).execute()


# ===========================================
# Claude API 설정
# ===========================================
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


# ===========================================
# Claude Vision - 이미지 분석
# ===========================================
def analyze_image_with_claude(image_bytes):
    prompt = """
문제 이미지에서 다음 두 가지를 JSON 형식으로 출력:
1) problem
2) formula
"""

    img_b64 = base64.b64encode(image_bytes).decode("utf-8")

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
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
        return result.get("problem", ""), result.get("formula", ""), None

    except Exception as e:
        return None, None, str(e)


# ===========================================
# 설명 생성
# ===========================================
def generate_explanation(problem_text, formula):
    prompt = f"""
전기기사 문제를 초보자도 이해할 수 있게 설명하시오.

문제: {problem_text}
공식: {formula}

1. 문제 해석  
2. 공식의 의미  
3. 풀이 과정  
4. 핵심 개념  
5. 암기 팁  
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1800,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text, None
    except Exception as e:
        return None, str(e)


# ===========================================
# UI 렌더링
# ===========================================

st.title("⚡ 전기기사 공식 AI 설명 생성기")

# ----------------------------
# 로그인 안 한 경우 로그인 화면 표시
# ----------------------------
if not st.session_state.user:
    tab1, tab2 = st.tabs(["로그인", "회원가입"])
    with tab1:
        login_ui()
    with tab2:
        signup_ui()
    st.stop()


# ===========================================
# 로그인 사용자 정보 표시
# ===========================================
user = st.session_state.user
usage_count = get_usage(user.id)

st.info(f"👤 {user.email} 님 | 오늘 사용량: **{usage_count}/{MAX_DAILY} 회**")

if usage_count >= MAX_DAILY:
    st.error("⚠️ 오늘 사용량 제한에 도달했습니다. 내일 다시 이용해주세요!")
    st.stop()


# ===========================================
# 이미지 업로드
# ===========================================
uploaded_file = st.file_uploader("📸 문제 이미지 업로드", type=["jpg", "jpeg", "png"])

auto_problem = ""
auto_formula = ""

if uploaded_file:
    st.info("이미지 분석 중...")
    image = Image.open(uploaded_file)

    if image.mode != "RGB":
        image = image.convert("RGB")

    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    img_bytes = buf.getvalue()

    problem, formula, err = analyze_image_with_claude(img_bytes)

    if err:
        st.error("이미지 분석 오류: " + err)
    else:
        auto_problem = problem
        auto_formula = formula

        st.success("이미지 분석 성공!")
        st.write("### 📘 문제")
        st.write(problem)
        st.write("### 📐 공식")
        st.write(formula)


# ===========================================
# 기존 문제 입력 필드
# ===========================================
st.divider()
problem_text = st.text_area("문제", value=auto_problem, height=150)
formula = st.text_input("공식", value=auto_formula)


# ===========================================
# 설명 생성 버튼
# ===========================================
if st.button("📖 설명 생성하기", type="primary"):

    if not problem_text or not formula:
        st.error("⚠️ 문제와 공식을 입력하세요.")
    else:
        with st.spinner("설명 생성 중..."):
            explanation, err = generate_explanation(problem_text, formula)

        if err:
            st.error(err)
        else:
            st.success("✨ 생성 완료!")

            # 사용량 증가
            increment_usage(user.id)

            st.markdown("### 📝 설명 결과")
            st.markdown(explanation)


            st.download_button(
                "📄 다운로드",
                explanation,
                file_name="electric_engineer_explanation.txt",
                mime="text/plain"
            )
