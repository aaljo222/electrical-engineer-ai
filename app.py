import streamlit as st
import anthropic
import os
import hashlib
import re
from datetime import datetime, timedelta

# ==========================
# 페이지 기본 설정
# ==========================
st.set_page_config(
    page_title="전기기사 공식 AI 설명 생성기",
    page_icon="⚡",
    layout="wide"
)

# ==========================
# API 키 설정
# ==========================
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# ==========================
# API 호출 제한 설정
# ==========================
DAILY_API_LIMIT = 50          # 하루 최대 50회
MONTHLY_TOKEN_LIMIT = 200000  # 월 20만 토큰

# 세션 상태 초기화
if "api_calls" not in st.session_state:
    st.session_state.api_calls = 0

if "token_usage" not in st.session_state:
    st.session_state.token_usage = 0

if "cache" not in st.session_state:
    st.session_state.cache = {}

# ==========================
# Google Drive 다운로드 추가
# ==========================

GOOGLE_DRIVE_LINKS = [
    "https://drive.google.com/file/d/1fcs1eizcmMFK0Bhh6si18Ljk0ajZf0Zv/view?usp=sharing",
    "https://drive.google.com/file/d/1aFcxtyQ8e70YFmvXkZfnheFKVqz7CaL-/view?usp=sharing",
    "https://drive.google.com/file/d/14DtoWF8vAVef5eTx_jLl7oyCMCwMQ1Ya/view?usp=sharing",
    "https://drive.google.com/file/d/1FdWbJkgjlqjnwE8yOOlESgH7ysr2HX1h/view?usp=sharing",
    "https://drive.google.com/file/d/13gwngdg70cHCwktfFotvm8rUVxB5-nlf/view?usp=sharing",
    "https://drive.google.com/file/d/1dbPncNCjAsGu6snuQ8Cpl0MlZ0WaWltv/view?usp=sharing",
    "https://drive.google.com/file/d/1dmVKaDfs3apH_ZQFkiK1u3wnIyQ64EEN/view?usp=sharing"
]

def extract_drive_id(url):
    match = re.search(r"/d/(.*?)/", url)
    if match:
        return match.group(1)
    return None

def get_download_url(url):
    file_id = extract_drive_id(url)
    if file_id:
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return None

# ==========================
# 다운로드 UI (기존 UI 위쪽에만 추가)
# ==========================

st.subheader("📥 전기 애니메이션 다운로드")

for url in GOOGLE_DRIVE_LINKS:
    dl = get_download_url(url)
    st.markdown(f"- [📌 다운로드 링크]({dl})")

st.divider()


# ==========================
# 해시 생성
# ==========================
def generate_hash(problem_text, formula):
    content = f"{problem_text}||{formula}"
    return hashlib.md5(content.encode()).hexdigest()


# ==========================
# Claude API 설명 생성 (제한 포함)
# ==========================
def generate_explanation(problem_text, formula):
    if not ANTHROPIC_API_KEY:
        return None, "API 키가 없습니다."

    # API 호출 제한
    if st.session_state.api_calls >= DAILY_API_LIMIT:
        return None, "⚠️ 오늘 API 호출 한도를 초과했습니다."

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""전기기사 시험 문제를 쉽게 설명해주세요.

문제: {problem_text}
공식: {formula}

다음 형식으로 작성하세요:
1. 문제 이해
2. 필요한 개념
3. 공식 유도
4. 예제 풀이
5. 암기 팁
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # 사용량 증가
        st.session_state.api_calls += 1
        st.session_state.token_usage += message.usage.output_tokens

        if st.session_state.token_usage > MONTHLY_TOKEN_LIMIT:
            return None, "⚠️ 월 토큰 한도를 초과했습니다."

        return message.content[0].text, None

    except Exception as e:
        return None, f"오류: {e}"


# ==========================
# 기존 UI (절대 수정하지 않음)
# ==========================

st.title("⚡ 전기기사 공식 AI 설명 생성기")
st.markdown("**Claude AI로 공식을 쉽게 이해하세요**")
st.divider()

# --- 사이드바 ---
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
    st.metric("생성된 설명", len(st.session_state.cache))

    st.divider()
    st.markdown("### API 사용량")
    st.write(f"오늘 호출: {st.session_state.api_calls} / {DAILY_API_LIMIT}")
    st.write(f"이번달 토큰: {st.session_state.token_usage} / {MONTHLY_TOKEN_LIMIT}")

    st.divider()
    st.markdown("Made with ❤️")

# --- 메인 입력 영역 ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 문제 입력")

    default_problem = st.session_state.get("selected_problem", "")
    default_formula = st.session_state.get("selected_formula", "")

    problem_text = st.text_area(
        "문제 내용",
        value=default_problem,
        height=150
    )

    formula = st.text_input(
        "관련 공식",
        value=default_formula
    )

with col2:
    st.subheader("ℹ️ 사용 방법")
    st.info("""
    1. 문제와 공식을 입력하세요
    2. 또는 예시를 클릭하세요
    3. '설명 생성' 버튼을 누르세요
    """)

    if ANTHROPIC_API_KEY:
        st.success("API 키 확인됨")
    else:
        st.error("API 키 없음")

st.divider()

# --- 설명 생성 버튼 ---
if st.button("📖 설명 생성하기", type="primary", use_container_width=True):

    if not problem_text or not formula:
        st.error("⚠ 문제/공식 입력 필요")
    else:
        content_hash = generate_hash(problem_text, formula)

        if content_hash in st.session_state.cache:
            st.success("⚡ 캐시 불러오기")
            explanation = st.session_state.cache[content_hash]
        else:
            with st.spinner("생성 중..."):
                explanation, error = generate_explanation(problem_text, formula)

                if error:
                    st.error(error)
                    explanation = None
                else:
                    st.session_state.cache[content_hash] = explanation
                    st.success("✨ 생성 완료!")

        if explanation:
            st.divider()
            st.subheader("✨ 생성 결과")
            st.markdown(explanation)

            st.download_button(
                "📋 텍스트 다운로드",
                explanation,
                file_name="전기기사_공식_설명.txt",
                mime="text/plain"
            )

# --- Footer ---
st.divider()
st.markdown("""
<div style='text-align:center; color:#666; padding:1rem;'>
전기기사 공식 AI 설명 생성기 | Powered by Claude API
</div>
""", unsafe_allow_html=True)
