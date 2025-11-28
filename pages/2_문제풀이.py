import streamlit as st
from core.ocr import analyze_image
from core.history import save_history
from core.auth import check_login
from anthropic import Anthropic
from PIL import Image
import io
import os

MODEL_SONNET = "claude-sonnet-4-5-20250929"

st.set_page_config(page_title="문제풀이", layout="wide")
st.title("📘 전기기사 문제 풀이")

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

user = check_login()

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

전기기사 문제를 단계적으로 상세하게 설명하세요.
"""

    with st.spinner("AI 생성 중..."):
        res = client.messages.create(
            model=MODEL_SONNET,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        explanation = res.content[0].text

    st.markdown(explanation)

    # 저장
    save_history(
        user["id"],
        problem,
        formula,
        explanation
    )
    st.success("기록 저장됨!")
