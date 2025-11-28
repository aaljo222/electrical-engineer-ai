import streamlit as st
from core.db import supabase
from core.auth import check_login
import random

st.title("📝 CBT 모의고사")
user = check_login()

problems = supabase.table("problems_master").select("*").limit(100).execute().data
random.shuffle(problems)

if "idx" not in st.session_state:
    st.session_state["idx"] = 0

i = st.session_state["idx"]
q = problems[i]

st.subheader(f"{i+1}. {q['question']}")
for c in q["choices"]:
    st.write(c)

answer = st.text_input("정답 입력")

if st.button("제출"):
    if answer == q["answer"]:
        st.success("정답!")
    else:
        st.error(f"오답! 정답: {q['answer']}")
    st.session_state["idx"] += 1
