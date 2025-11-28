import streamlit as st
from core.auth import check_login
from core.explain import make_explanation, grade_answer
from core.history import save_history
from core.ocr import analyze_image   # 🔥 이미지 분석 추가
from core.db import supabase

user = check_login()

st.title("📘 문제 풀이")

# ---------------------------------------------------
# 이미지 업로드 + OCR 분석
# ---------------------------------------------------
st.subheader("문제 이미지 업로드 (선택)")
uploaded = st.file_uploader("문제 사진을 선택하세요", type=["jpg", "jpeg", "png"])

problem_text = ""

if uploaded:
    st.image(uploaded, caption="업로드한 문제", use_column_width=True)
    with st.spinner("OCR 분석 중..."):
        ocr_result = analyze_image(uploaded)
    if ocr_result:
        st.success("OCR 텍스트 추출 완료!")
        problem_text = ocr_result
    else:
        st.error("OCR 분석 실패")

# ---------------------------------------------------
# 문제 텍스트
# ---------------------------------------------------
st.subheader("문제 설명")
problem = st.text_area("문제 입력", value=problem_text, height=200)

# ---------------------------------------------------
# 사용자 풀이식 / 정답
# ---------------------------------------------------
formula = st.text_area("풀이 공식(선택)", placeholder="예: P = VI")
correct_answer = st.text_input("정답 (정답이 있을 경우)")
user_answer = st.text_input("내 답안")

# ---------------------------------------------------
# 채점 + AI 풀이 + DB 저장
# ---------------------------------------------------
if st.button("정답 확인"):
    if not problem.strip():
        st.error("문제 내용을 입력하거나 이미지 업로드로 문제를 불러오세요.")
        st.stop()

    with st.spinner("AI 채점 중..."):
        result = grade_answer(problem, user_answer, correct_answer if correct_answer else "")
        explanation = make_explanation(problem, formula if formula else "")

        save_history(
            user_id=user["id"],
            problem=problem,
            formula=formula,
            explanation=explanation,
        )

    # -----------------------
    # 결과 출력
    # -----------------------
    st.success("채점 완료!")

    if "is_correct" in result:
        if result["is_correct"]:
            st.success("⭕ 정답입니다!")
        else:
            st.error("❌ 오답입니다.")

    st.markdown("### 📗 채점 사유")
    st.write(result.get("reason", ""))

    st.markdown("---")
    st.markdown("### 📘 AI 풀이 설명")
    st.write(explanation)
