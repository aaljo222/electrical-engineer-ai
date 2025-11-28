import streamlit as st
from core.db import supabase
from core.auth import get_user
from core.history import save_history
from core.explain import make_explanation

st.title("📝 CBT 모의고사")

user = get_user()
if not user:
    st.warning("로그인 해주세요.")
    st.stop()

q = supabase.table("problems_master").select("*").limit(1).execute().data[0]

st.write("### 문제")
st.write(q["question"])

user_answer = st.text_input("당신의 답:")

if st.button("채점"):
    explanation = make_explanation(q["question"])
    save_history(user["id"], q["question"], q["formula"], explanation)

    st.success("저장 완료!")
    st.write(explanation)
