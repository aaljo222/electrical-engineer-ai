import streamlit as st
from core.db import supabase
from core.auth import check_login

st.title("📊 나의 학습 통계")
user = check_login()

history = supabase.table("user_history").select("*").eq("user_id", user.id).execute().data

st.write(f"총 학습 문제 수: {len(history)}")

subjects = {}
for h in history:
    subj = h.get("subject", "미정")
    subjects[subj] = subjects.get(subj, 0) + 1

st.bar_chart(subjects)
