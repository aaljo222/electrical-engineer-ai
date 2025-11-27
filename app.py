import streamlit as st
import anthropic
import os
import hashlib
import re
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="전기기사 공식 AI 설명 생성기",
    page_icon="⚡",
    layout="wide"
)

# API 설정
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# Google Drive 파일 리스트
GOOGLE_DRIVE_LINKS = [
    "https://drive.google.com/file/d/1fcs1eizcmMFK0Bhh6si18Ljk0ajZf0Zv/view?usp=sharing",
    "https://drive.google.com/file/d/1aFcxtyQ8e70YFmvXkZfnheFKVqz7CaL-/view?usp=sharing",
    "https://drive.google.com/file/d/14DtoWF8vAVef5eTx_jLl7oyCMCwMQ1Ya/view?usp=sharing",
    "https://drive.google.com/file/d/1FdWbJkgjlqjnwE8yOOlESgH7ysr2HX1h/view?usp=sharing",
    "https://drive.google.com/file/d/13gwngdg70cHCwktfFotvm8rUVxB5-nlf/view?usp=sharing",
    "https://drive.google.com/file/d/1dbPncNCjAsGu6snuQ8Cpl0MlZ0WaWltv/view?usp=sharing",
    "https://drive.google.com/file/d/1dmVKaDfs3apH_ZQFkiK1u3wnIyQ64EEN/view?usp=sharing"
]

# --- API 사용 제한 설정 ---
DAILY_API_LIMIT = 5                # 하루 최대 호출 횟수
MONTHLY_TOKEN_LIMIT = 200_000       # 월 최대 토큰 제한

# 세션 상태 초기화
if "cache" not in st.session_state:
    st.session_state.cache = {}

if "api_calls" not in st.session_state:
    st.session_state.api_calls = 0

if "token_usage" not in st.session_state:
    st.session_state.token_usage = 0

if "reset_time" not in st.session_state:
    st.session_state.reset_time = datetime.now() + timedelta(days=1)


# --- Google Drive ID 추출 ---
def extract_drive_id(url):
    match = re.search(r"/d/(.*?)/", url)
    if match:
        return match.group(1)
    return None

# --- 다운로드 URL 변환 ---
def get_download_url(url):
    file_id = extract_drive_id(url)
    if not file_id:
        return None
    return f"https://drive.google.com/uc?export=download&id={file_id}"


# --- 해시 생성 ---
def generate_hash(problem_text, formula):
    content = f"{problem_text}||{formula}"
    return hashlib.md5(content.encode()).hexdigest()


# --- Claude API 설명 생성 ---
def generate_explanation(problem_text, formula):
    if not ANTHROPIC_API_KEY:
        return None, "API 키가 없습니다."

    # API 호출 제한 체크
    if st.session_state.api_calls >= DAILY_API_LIMIT:
        return None, "⚠️ 오늘의 API 호출 한도(50회)를 모두 사용했습니다."

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""
    전기기사 시험 문제를 쉽게 설명해주세요.

    문제: {problem_text}
    공식: {formula}

    다음 형식으로 단계별 설명을 작성하세요:
    - 문제 이해
    - 필요한 개념
    - 공식 유도
    - 예제 풀이
    - 암기 팁

    한글로 친절하게 설명해주세요.
    """

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250421",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        # API 사용량 증가
        st.session_state.api_calls += 1
        st.session_state.token_usage += message.usage.output_tokens

        if st.session_state.token_usage > MONTHLY_TOKEN_LIMIT:
            return None, "⚠️ 월 토큰 한도를 초과했습니다. (200,000 tokens)"

        return message.content[0].text, None

    except Exception as e:
        return None, str(e)


# --- UI 시작 ---
st.title("⚡ 전기기사 공식 AI 설명 생성기")
st.divider()

# ▼ Google Drive 다운로드 섹션
st.subheader("🎥 공식 전기 애니메이션 자료 다운로드")
for url in GOOGLE_DRIVE_LINKS:
    dl = get_download_url(url)
    st.markdown(f"- [📥 다운로드]({dl})  |  {url}")

st.divider()

# ▼ 문제 입력 UI
col1, col2 = st.columns([2, 1])

with col1:
    problem_text = st.text_area("문제 입력", height=150)
    formula = st.text_input("관련 공식 입력")

with col2:
    st.info(f"""
    **API 사용량 현황**
    - 오늘 사용: {st.session_state.api_calls} / {DAILY_API_LIMIT} 회
    - 이번 달 토큰 사용량: {st.session_state.token_usage} / {MONTHLY_TOKEN_LIMIT} tokens
    """)
    st.success("API 키 설정됨" if ANTHROPIC_API_KEY else "API 키 없음")

st.divider()

# ▼ 설명 생성 버튼 처리
if st.button("📘 설명 생성"):
    if not problem_text or not formula:
        st.error("⚠️ 문제와 공식을 입력하세요.")
    else:
        h = generate_hash(problem_text, formula)

        if h in st.session_state.cache:
            explanation = st.session_state.cache[h]
            st.success("⚡ 캐시 사용")
        else:
            explanation, err = generate_explanation(problem_text, formula)
            if err:
                st.error(err)
                explanation = None
            else:
                st.session_state.cache[h] = explanation

        if explanation:
            st.markdown("### ✨ 생성된 설명")
            st.markdown(explanation)

            st.download_button(
                "📄 설명 텍스트 다운로드",
                explanation,
                "전기기사_AI_설명.txt",
                mime="text/plain"
            )

st.divider()
st.markdown("<p style='text-align:center;'>Made by Jaeoh Lee ⚡</p>", unsafe_allow_html=True)
