import streamlit as st
from core.auth import check_login
from core.explain import make_explanation, grade_answer
from core.history import save_history
from core.db import supabase

user = check_login()

st.title("문제 풀이")

# ----------------------------
# 문제 불러오기
# ----------------------------
problem = st.text_area("문제 설명", height=150)
formula = st.text_area("풀이 공식")
correct_answer = st.text_input("정답")
user_answer = st.text_input("내 답안")

# ----------------------------
# 채점 & 저장
# ----------------------------
if st.button("정답 확인"):
    with st.spinner("AI 채점 중..."):
        result = grade_answer(problem, user_answer, correct_answer)
        explanation = make_explanation(problem, formula)

        save_history(
            user_id=user["id"],
            problem=problem,
            formula=formula,
            explanation=explanation,
        )

    st.success("채점 완료")
    st.write(result["reason"])
    st.markdown("### 📘 AI 풀이 설명")
    st.write(explanation)
