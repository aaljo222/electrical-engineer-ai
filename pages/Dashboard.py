import streamlit as st
import pandas as pd
import plotly.express as px
from core.db import get_supabase
from core.auth import check_login
from core.explain import ai_coach_feedback

st.set_page_config(page_title="대시보드", layout="wide")
st.title("📊 사용자 학습 대시보드")

user = check_login()
supabase = get_supabase()

# -----------------------
# 1) 데이터 로드
# -----------------------
history = (
    supabase.table("user_history")
    .select("id, problem, formula")
    .eq("user_id", user["id"])
    .execute()
).data

wrong = (
    supabase.table("user_wrongbook")
    .select("problem_id")
    .eq("user_id", user["id"])
    .execute()
).data

total = len(history)
wrong_cnt = len(wrong)
acc = round((total - wrong_cnt) / total * 100, 1) if total else 0

st.metric("전체 정답률", f"{acc} %")
st.metric("풀이 수", total)
st.metric("오답 수", wrong_cnt)

# -----------------------
# 2) 과목별 정답률
# -----------------------
all_problems = (
    supabase.table("problems_master")
    .select("*")
    .execute()
).data

if all_problems:
    df = pd.DataFrame(all_problems)
    wrong_ids = [x["problem_id"] for x in wrong]

    df["is_wrong"] = df["id"].isin(wrong_ids)
    subject_stats = df.groupby("subject")["is_wrong"].mean().reset_index()
    subject_stats["accuracy"] = 100 - subject_stats["is_wrong"] * 100

    st.subheader("📘 과목별 정답률")
    fig = px.bar(subject_stats, x="subject", y="accuracy", title="과목별 정확도")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 3) AI 학습 전략
# -----------------------
if st.button("🧠 AI 맞춤 학습 전략 생성"):
    feedback = ai_coach_feedback(history, wrong)
    st.markdown("### 🧠 학습 전략")
    st.write(feedback)
