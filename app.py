import streamlit as st
import anthropic
import os
import hashlib

# 페이지 설정
st.set_page_config(
    page_title="전기기사 공식 AI 설명 생성기",
    page_icon="⚡",
    layout="wide"
)

# API 키 설정
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# 세션 상태 초기화 (캐시)
if 'cache' not in st.session_state:
    st.session_state.cache = {}

def generate_hash(problem_text, formula):
    """해시 생성"""
    content = f"{problem_text}||{formula}"
    return hashlib.md5(content.encode()).hexdigest()

def generate_explanation(problem_text, formula):
    """Claude API로 설명 생성"""
    
    if not ANTHROPIC_API_KEY:
        return None, "API 키가 설정되지 않았습니다. Streamlit Secrets에 ANTHROPIC_API_KEY를 추가해주세요."
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    prompt = f"""전기기사 시험 문제를 쉽게 설명해주세요.

문제: {problem_text}
공식: {formula}

다음 형식으로 단계별 설명을 작성하세요:

## 1. 문제 이해
[문제를 쉽게 풀어서 설명]

## 2. 필요한 개념
[관련 개념 설명]

## 3. 공식 유도
[공식을 어떻게 유도하는지 단계별로]

## 4. 예제 풀이
[구체적인 숫자를 넣어서 예제 문제 풀이]

## 5. 암기 팁
[공식을 쉽게 외우는 방법]

한글로 친절하게 설명해주세요. 마크다운 형식으로 작성하되, 수식은 LaTeX 없이 일반 텍스트로 표현하세요.
"""
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text, None
    except Exception as e:
        return None, f"오류 발생: {str(e)}"

# 헤더
st.title("⚡ 전기기사 공식 AI 설명 생성기")
st.markdown("**Claude AI로 공식을 쉽게 이해하세요**")
st.divider()

# 사이드바 - 예시 문제
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
    st.markdown("### 📊 통계")
    st.metric("생성된 설명", len(st.session_state.cache))
    
    st.divider()
    st.markdown("**Made with ❤️**")
    st.markdown("Claude API & Streamlit")

# 메인 영역
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 문제 입력")
    
    # 예시 선택 시 자동 입력
    default_problem = st.session_state.get('selected_problem', '')
    default_formula = st.session_state.get('selected_formula', '')
    
    problem_text = st.text_area(
        "문제 내용",
        value=default_problem,
        height=150,
        placeholder="예시: 평행판 커패시터의 극판 사이에 유전체를 채웠을 때 정전용량의 변화를 구하시오."
    )
    
    formula = st.text_input(
        "관련 공식",
        value=default_formula,
        placeholder="예시: C = ε₀εᵣA/d"
    )

with col2:
    st.subheader("ℹ️ 사용 방법")
    st.info("""
    1. 문제와 공식을 입력하세요
    2. 또는 왼쪽 예시를 클릭하세요
    3. "설명 생성" 버튼을 누르세요
    4. 10-20초 후 설명이 나타납니다
    """)
    
    if ANTHROPIC_API_KEY:
        st.success("✅ API 키 설정됨")
    else:
        st.error("❌ API 키가 필요합니다")

st.divider()

# 생성 버튼
if st.button("📖 설명 생성하기", type="primary", use_container_width=True):
    if not problem_text or not formula:
        st.error("⚠️ 문제와 공식을 모두 입력해주세요.")
    else:
        # 해시 생성
        content_hash = generate_hash(problem_text, formula)
        
        # 캐시 확인
        if content_hash in st.session_state.cache:
            st.success("⚡ 캐시된 결과를 불러왔습니다!")
            explanation = st.session_state.cache[content_hash]
        else:
            # 로딩 표시
            with st.spinner("Claude가 설명을 작성하고 있습니다... (10-30초 소요)"):
                explanation, error = generate_explanation(problem_text, formula)
                
                if error:
                    st.error(f"오류: {error}")
                    explanation = None
                else:
                    # 캐시에 저장
                    st.session_state.cache[content_hash] = explanation
                    st.success("✨ 설명 생성 완료!")
        
        # 결과 표시
        if explanation:
            st.divider()
            st.subheader("✨ 생성 결과")
            
            # 마크다운으로 표시
            st.markdown(explanation)
            
            # 복사 버튼
            st.download_button(
                label="📋 텍스트 다운로드",
                data=explanation,
                file_name="전기기사_공식_설명.txt",
                mime="text/plain"
            )

# 푸터
st.divider()
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 2rem;'>
    <p>전기기사 공식 AI 설명 생성기 | Powered by Claude API & Streamlit</p>
    <p>23년 임베디드 개발 경력 | 7년 전기 교육 강사</p>
</div>
""", unsafe_allow_html=True)
