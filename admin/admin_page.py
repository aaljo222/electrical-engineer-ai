import streamlit as st
import json
import base64
from supabase import create_client
from extractor import extract_pdf_to_json
import os

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"]
)

st.title("📚 전기기사 문제은행 관리자 페이지")

if "admin" not in st.session_state:
    st.session_state.admin = True   # 데모상 자동 관리자 로그인

uploaded = st.file_uploader("기출문제 PDF 업로드", type=["pdf"])

if uploaded:
    pdf_path = "uploaded.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded.read())

    st.info("📄 PDF → JSON 변환 중…")

    extract_pdf_to_json(pdf_path, "problems.json")

    with open("problems.json", "r", encoding="utf-8") as f:
        problems = json.load(f)

    st.success(f"{len(problems)}문제 분석 완료")

    if st.button("📥 Supabase 문제은행 저장"):
        for p in problems:
            supabase.table("problems_master").insert({
                "year": 2022,
                "session": 2,
                "subject": "회로이론",
                "question_no": p["id"],
                "question": p["question"],
                "choices": p.get("choices"),
                "answer": p.get("answer"),
                "formula": p.get("formula"),
            }).execute()

        st.success("저장 완료!")
