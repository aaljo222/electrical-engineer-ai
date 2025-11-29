import streamlit as st
from core.auth import check_login
from core.ocr import extract_text_from_image
from core.explain import solve_problem
from core.history import save_history

user = check_login()

st.title("🧠 문제 OCR + AI 풀이")

uploaded_file = st.file_uploader("문제 이미지 업로드", type=["png", "jpg", "jpeg"])


def parse_claude_answer(answer: str):
    """
    Claude의 구조화된 답변을 정확하게 파싱하여
    formula(정답), explanation(풀이)만 분리
    """

    formula = ""
    explanation = ""

    # 구간 나누기
    if "정답:" in answer:
        formula = answer.split("정답:")[1].split("상세")[0].strip()

    if "상세 풀이 과정:" in answer:
        explanation = answer.split("상세 풀이 과정:")[1]
        # "사용된 개념:" 이전까지만 추출
        if "사용된 개념:" in explanation:
            explanation = explanation.split("사용된 개념:")[0]

    return formula.strip(), explanation.strip()


if uploaded_file:
    st.image(uploaded_file, caption="업로드된 문제 이미지")

    with st.spinner("OCR 처리 중..."):
        problem_text = extract_text_from_image(uploaded_file)

    st.subheader("📘 OCR 결과")
    st.text(problem_text)

    if st.button("🧠 AI 풀이 생성"):
        with st.spinner("Claude가 문제를 분석 중..."):
            raw_answer = solve_problem(problem_text)

        formula, explanation = parse_claude_answer(raw_answer)

        st.subheader("📘 정답")
        st.write(formula)

        st.subheader("🧩 풀이 과정")
        st.markdown(explanation.replace("\n", "  \n"), unsafe_allow_html=True)

        # ✔ save_history()를 사용하여 올바르게 저장
        save_history(
            user_id=user["id"],
            problem=problem_text,
            formula=formula,
            explanation=explanation
        )

        st.success("✔ 저장 완료!")
