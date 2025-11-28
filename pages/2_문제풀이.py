import streamlit as st
from core.ocr import analyze_image
from core.explain import make_explanation, grade_answer
from core.history import save_history
from core.db import supabase
from core.auth import check_login

import io
from PIL import Image
from anthropic import Anthropic
import os

st.title("📘 전기기사 문제 풀이")

user = check_login()
user_id = user["id"]

uploaded = st.file_uploader("문제 이미지 업로드", type=["png", "jpg", "jpeg"])

problem_text = ""
formula = ""
problem_id = None

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    problem_id, problem_text, formula = analyze_image(image_bytes)

    if problem_id is None:
        st.error("문제를 찾을 수 없습니다.")
    else:
        st.success(f"문제 인식 완료 (ID: {problem_id})")

problem_text = st.text_area("문제", problem_text)
formula = st.text_input("공식", formula)
user_answer = st.text_input("나의 풀이")

if st.button("설명 생성"):
    if not problem_id:
        st.error("먼저 문제 이미지 또는 문제 텍스트가 필요합니다.")
    else:
        # 정답 가져오기
        correct_row = (
            supabase.table("problems_master")
            .select("answer")
            .eq("id", problem_id)
            .single()
            .execute()
        ).data

        correct_answer = correct_row["answer"]

        # 채점
        is_correct = grade_answer(correct_answer, user_answer)

        # 설명 생성
        explanation = make_explanation(problem_text, formula)
        st.markdown(explanation)

        # 저장
        save_history(
            user_id=user_id,
            problem_id=problem_id,
            user_answer=user_answer,
            explanation=explanation,
            is_correct=is_correct,
        )

        st.success("기록 저장 완료!")

        # 오답이면 오답노트 저장
        if not is_correct:
            supabase.table("user_wrongbook").insert({
                "user_id": user_id,
                "problem_id": problem_id,
                "user_answer": user_answer,
            }).execute()
            st.warning("오답노트에 저장되었습니다!")
