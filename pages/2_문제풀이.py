import streamlit as st
from core.auth import check_login
from core.ocr import extract_text_from_image
from core.explain import solve_problem
from core.db import supabase

user = check_login()

st.title("🧠 문제 OCR + AI 풀이 생성")

uploaded_file = st.file_uploader("문제 이미지 업로드", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="업로드된 문제 이미지")

    with st.spinner("🔍 OCR 처리 중..."):
        extracted_text = extract_text_from_image(uploaded_file)
    
    st.subheader("📘 OCR 결과(문제 텍스트)")
    st.text(extracted_text)

    if st.button("🧠 AI 문제 풀이 생성"):
        with st.spinner("Claude가 문제를 분석 중입니다..."):
            solution = solve_problem(extracted_text)

        st.subheader("📘 AI 생성 문제 풀이")
        st.write(solution)

        # Supabase 저장
        supabase.table("history").insert({
            "user_id": user["id"],
            "problem_text": extracted_text,
            "solution": solution
        }).execute()

        st.success("기록이 저장되었습니다.")
