import streamlit as st
from core.ocr import analyze_image
from core.history import save_history
from anthropic import Anthropic
import os
from PIL import Image
import io

if "user" not in st.session_state:
    st.switch_page("pages/1_로그인.py")

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-3-5-sonnet-20240620"   # ← 바로 이 모델이 정답!

st.title("📘 전기기사 문제 풀이")

uploaded = st.file_uploader("문제 이미지 업로드", type=["png", "jpg", "jpeg"])

problem = ""
formula = ""

if uploaded:
    img = Image.open(uploaded)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG")
    problem, formula = analyze_image(buf.getvalue())

problem = st.text_area("문제", problem)
formula = st.text_input("공식", formula)

if st.button("설명 생성"):
    prompt = f"""
문제: {problem}
공식: {formula}

전기기사 문제를 단계적으로 설명하세요.
"""

    with st.spinner("AI 생성 중..."):
        res = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        explanation = res.content[0].text

    st.markdown(explanation)

    save_history(
        st.session_state["user"]["id"],
        problem,
        formula,
        explanation
    )
