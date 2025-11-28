import streamlit as st
from core.ocr import analyze_image
from core.explain import solve_problem

st.title("📘 문제 풀이")

uploaded = st.file_uploader("문제 사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded:
    st.success("이미지가 업로드되었습니다.")

    # OCR
    with st.spinner("이미지를 분석 중입니다. 잠시만 기다려주세요..."):
        ocr_text = analyze_image(uploaded)

    st.subheader("📄 OCR 인식 결과")
    st.write(ocr_text)

    if st.button("문제 풀이 생성"):
        with st.spinner("AI가 풀이를 생성 중입니다..."):
            result = solve_problem(ocr_text)

        st.subheader("🧠 AI 풀이 결과")
        st.write(result)
