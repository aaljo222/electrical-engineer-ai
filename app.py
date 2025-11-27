import streamlit as st
import anthropic
import hashlib
import os
import re
from PIL import Image
import io


# ==========================
# 페이지 설정
# ==========================
st.set_page_config(
    page_title="전기기사 공식 AI 설명 생성기",
    page_icon="⚡",
    layout="wide"
)

# ==========================
# API
# ==========================
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


# ==========================
# Claude Vision: 이미지 분석 함수
# ==========================
def analyze_image_with_claude(image_bytes):
    prompt = """
당신은 이미지 속 전기기사 시험 문제를 분석하여 아래 두 가지만 추출합니다.

1) 문제 내용
2) 공식

출력 형식은 반드시 아래 JSON 형식으로만 출력하세요:

{
 "problem": "...",
 "formula": "..."
}
"""

    try:
        message = client.messages.create(
            model="claude-3-opus-vision",
            max_tokens=1200,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image": image_bytes,
                            "media_type": "image/jpeg"
                        }
                    ]
                }
            ]
        )

        import json
        result = json.loads(message.content[0].text)

        return result.get("problem", ""), result.get("formula", ""), None

    except Exception as e:
        return None, None, f"이미지 분석 오류: {e}"


# ==========================
# 해시
# ==========================
def generate_hash(problem_text, formula):
    return hashlib.md5(f"{problem_text}||{formula}".encode()).hexdigest()


# ==========================
# 문제 설명 생성
# ==========================
def generate_explanation(problem_text, formula):
    if not ANTHROPIC_API_KEY:
        return None, "API 키가 없습니다."

    prompt = f"""
전기기사 시험 문제를 쉽게 설명해주세요.

문제: {problem_text}
공식: {formula}

다음 항목으로 설명하세요:
1. 문제 이해
2. 필요한 개념
3. 공식 유도
4. 예제 풀이
5. 암기 팁
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1800,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text, None
    except Exception as e:
        return None, str(e)




# ==========================
# UI 시작
# ==========================
st.title("⚡ 전기기사 공식 AI 설명 생성기")
st.markdown("**Claude Vision + Sonnet으로 문제/공식을 자동 분석하고 해설을 생성합니다.**")
st.divider()


# ============================================================
# 📷 이미지 업로드 (UI 상단, 기존 UI 변경 없음)
# ============================================================
uploaded_file = st.file_uploader("📸 문제/공식 이미지 업로드", type=["jpg", "jpeg", "png"])

auto_problem = ""
auto_formula = ""

if uploaded_file:
    st.info("이미지 분석 중... (Claude Vision 처리)")

    # 이미지 열기
    image = Image.open(uploaded_file)

    # RGBA → RGB 변환
    if image.mode != "RGB":
        image = image.convert("RGB")

    # JPEG 바이트 변환
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes = img_bytes.getvalue()

    # Claude Vision OCR 호출
    problem, formula, error = analyze_image_with_claude(img_bytes)

    if error:
        st.error(error)
    else:
        auto_problem = problem
        auto_formula = formula

        st.success("사진 분석 성공! 아래 입력칸에 자동 적용됩니다.")
        st.markdown("### 📘 추출된 문제")
        st.write(problem)
        st.markdown("### 📐 추출된 공식")
        st.write(formula)

st.divider()


# ============================================================
# 📌 기존 사이드바 UI 그대로 복구
# ============================================================
with st.sidebar:
    st.header("💡 예시 문제")

    examples = {
        "커패시턴스 변화": {
            "problem": "평행판 커패시터 사이에 유전율 εᵣ인 유전체를 채웠을 때, 정전용량이 어떻게 변하는가?",
            "formula": "C = ε₀εᵣA/d"
        },
        "공진 주파수": {
            "problem": "RLC 직렬 회로에서 공진 주파수를 구하시오.",
            "formula": "f₀ = 1/(2π√LC)"
        },
        "임피던스": {
            "problem": "임피던스 Z = R + jX에서 R과 X의 관계를 설명하시오.",
            "formula": "|Z| = √(R² + X²)"
        }
    }

    for title, content in examples.items():
        if st.button(title, use_container_width=True):
            st.session_state.selected_problem = content["problem"]
            st.session_state.selected_formula = content["formula"]

    st.divider()
    st.markdown("Made with ❤️")


# ============================================================
# 문제 입력 UI (그대로 유지)
# ============================================================
default_problem = st.session_state.get("selected_problem", auto_problem)
default_formula = st.session_state.get("selected_formula", auto_formula)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 문제 입력")
    problem_text = st.text_area("문제 내용", value=default_problem, height=150)
    formula = st.text_input("관련 공식", value=default_formula)

with col2:
    st.subheader("ℹ️ 사용 방법")
    st.info("""
1. 문제/공식 사진을 업로드하면 자동 입력됩니다.
2. 또는 왼쪽 예시를 클릭하세요.
3. 문제/공식을 입력한 뒤 '설명 생성하기'를 누르세요.
""")


st.divider()


# ============================================================
# 설명 생성 버튼
# ============================================================
if st.button("📖 설명 생성하기", type="primary", use_container_width=True):

    if not problem_text or not formula:
        st.error("⚠️ 문제/공식을 입력하거나 사진을 업로드하세요.")
    else:
        explanation, error = generate_explanation(problem_text, formula)

        if error:
            st.error(error)
        else:
            st.success("✨ 설명 생성 완료!")
            st.markdown("### ✨ 생성 결과")
            st.markdown(explanation)

            st.download_button(
                "📋 텍스트 다운로드",
                explanation,
                "전기기사_공식_설명.txt",
                "text/plain"
            )
