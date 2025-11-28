import streamlit as st
from core.auth import check_login
from core.explain import make_explanation, grade_answer
from core.history import save_history
from core.ocr import analyze_image

user = check_login()

st.title("📘 문제 풀이")

# ---------------------------------------------------
# 이미지 업로드 & OCR
# ---------------------------------------------------
st.subheader("문제 이미지 업로드 (선택)")

uploaded = st.file_uploader("문제 사진 업로드", type=["jpg", "jpeg", "png"])

# 입력창 초기값
if "problem_text" not in st.session_state:
    st.session_state.problem_text = ""

if "formula_text" not in st.session_state:
    st.session_state.formula_text = ""

if uploaded:
    st.info("이미지를 분석 중입니다. 잠시만 기다려주세요...")
    with st.spinner("OCR 분석 중..."):
        ocr_text = analyze_image(uploaded)

    if ocr_text:
        st.success("OCR 텍스트 추출 완료!")

        # 🔥 자동으로 문제 + 공식 입력란에 채워넣기
        st.session_state.problem_text = ocr_text
        st.session_state.formula_text = ""   # 공식은 일반적으로 OCR로 정확히 못 뽑으므로 비움
    else:
        st.error("OCR 분석 실패!")


# ---------------------------------------------------
# 문제 입력 창 (OCR 결과 자동 반영)
# ---------------------------------------------------
st.subheader("문제")
problem = st.text_area(
    "문제를 입력하세요",
    value=st.session_state.problem_text,
    key="problem_input",
    height=150
)

# ---------------------------------------------------
# 공식 입력 창 (OCR 자동 입력 가능)
# ---------------------------------------------------
st.subheader("풀이 공식 (선택)")
formula = st.text_area(
    "공식 입력",
    value=st.session_state.formula_text,
    key="formula_input",
    height=100
)

# ---------------------------------------------------
# 사용자 정답/AI 채점
# ---------------------------------------------------
correct_answer = st.text_input("정답 (있는 경우)")
user_answer = st.text_input("내 답")

# ---------------------------------------------------
# 채점 + 설명 생성 + DB 저장
# ---------------------------------------------------
if st.button("정답 확인"):
    if not problem.strip():
        st.error("문제 내용을 입력하거나 OCR을 사용하세요.")
        st.stop()

    with st.spinner("AI 채점 중..."):
        result = grade_answer(problem, user_answer, correct_answer)
        explanation = make_explanation(problem, formula)

        save_history(
            user_id=user["id"],
            problem=problem,
            formula=formula,
            explanation=explanation,
        )

    st.success("채점 완료!")

    if result.get("is_correct"):
        st.success("⭕ 정답입니다!")
    else:
        st.error("❌ 오답입니다.")

    st.write("### 📌 채점 근거")
    st.write(result.get("reason", ""))

    st.write("---")
    st.write("### 📘 AI 풀이 설명")
    st.write(explanation)
