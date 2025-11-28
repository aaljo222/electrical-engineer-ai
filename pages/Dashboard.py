import streamlit as st
import pandas as pd
import plotly.express as px
from core.db import supabase
from core.auth import check_login
from core.explain import ai_coach_feedback

st.set_page_config(layout="wide")
st.title("📊 사용자 수준 분석 대시보드")

user = check_login()

# -----------------------------
# 1) 사용자 기록 불러오기
# -----------------------------
history = (
    supabase.table("user_history")
    .select("*")
    .eq("user_id", user.id)
    .execute()
).data

wrong = (
    supabase.table("user_wrongbook")
    .select("problem_id")
    .eq("user_id", user.id)
    .execute()
).data

# -----------------------------
# 2) 통계 처리
# -----------------------------
total_solved = len(history)
total_wrong = len(wrong)
correct = total_solved - total_wrong
accuracy = round(correct / total_solved * 100, 1) if total_solved else 0

st.metric("전체 정답률", f"{accuracy} %")
st.metric("전체 풀이 수", total_solved)
st.metric("오답 수", total_wrong)

# -----------------------------
# 3) 과목별 정답률
# -----------------------------
problems = supabase.table("problems_master").select("*").execute().data
problem_df = pd.DataFrame(problems).set_index("id")

wrong_ids = [x["problem_id"] for x in wrong]
history_ids = [x["problem_id"] for x in history]

df = problem_df.loc[history_ids]
df["is_wrong"] = df.index.isin(wrong_ids)

subject_stats = df.groupby("subject")["is_wrong"].mean().reset_index()
subject_stats["accuracy"] = 100 - subject_stats["is_wrong"] * 100

st.subheader("📘 과목별 정답률")
st.plotly_chart(
    px.bar(subject_stats, x="subject", y="accuracy", title="과목별 정확도 (%)"),
    use_container_width=True
)

# -----------------------------
# 4) AI 기반 맞춤 학습 조언
# -----------------------------
if st.button("🧠 AI가 나의 학습 전략 생성하기"):
    feedback = ai_coach_feedback(history, wrong)
    st.markdown("### 🧠 AI 학습 코치의 조언")
    st.write(feedback)
