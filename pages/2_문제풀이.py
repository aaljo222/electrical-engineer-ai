import streamlit as st
from core.auth import require_login
from core.ocr import analyze_image
from core.history import save_history
import anthropic

require_login()

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_KEY"])
st.title("📘 전기기사 문제풀이")

uploaded = st.file_uploader("문제 이미지 업로드", type=["jpg", "png", "jpeg"])

problem = ""
formula = ""

if uploaded:
    img = uploaded.read()
    data = analyze_image(img)
    problem = data["problem"]
    formula = data["formula"]

problem_text = st.text_area("문제", problem)
formula_text = st.text_input("공식", formula)

if st.button("설명 생성"):
    prompt = f"""
전기기사 문제를 단계별로 설명하세요.

문제: {problem_text}
공식: {formula_text}
"""
    res = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    explanation = res.content[0].text
    st.markdown(explanation)

    save_history(st.session_state.user["id"], problem_text, formula_text, explanation)
