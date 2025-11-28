import anthropic
import os
import streamlit as st

st.title("현재 Anthropic 계정에서 사용 가능한 모델 목록")

try:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    models = client.models.list()

    st.subheader("✔ 사용 가능한 모델들")
    for m in models.data:
        st.write("-", m.id)

except Exception as e:
    st.error("❌ 오류 발생")
    st.error(str(e))
