import streamlit as st
import pandas as pd
import plotly.express as px

from core.db import get_supabase
from core.auth import check_login
from core.explain import ai_coach_feedback

# -----------------------------
# 초기 설정
# -----------------------------
st.set_page_config(layout="wide")
st.title("📊 사용자 수준 분석 대시보드")

# Supabase 객체 생성
supabase = get_supabase()

# 로그인 체크
user = check_login()
if not user:
    st.error("로그인이 필요합니다.")
    st.stop()

# -------------------------------------
# 1) 사용자 풀이 기록 불러오기
# -------------------------------------
history_res = (
    supabase.table("user_history")
    .select("*")
    .eq("user_id", user["id"])
    .execute()
)

wrong_res = (
    supabase.table("user_wrongbook")
    .select("problem_id")
    .eq("user_id", user["id"])
    .execute()
)

history = history_res.data or []
wrong = wrong_res.data or []

# -------------------------------------
# 2) 통계 계산
# -------------------------------------
total_solved = len(history)
total_wrong = len(wrong)
correct = total_solved - total_wrong
accuracy = round(correct / total_solved * 100, 1) if total_solved else 0

col1, col2, col3 = st.columns(3)
col1.metric("전체 정답률", f"{accuracy} %")
col2.metric("전체 풀이 수", total_solved)
col3.metric("오답 수", total_wrong)

# -------------------------------------
# 3) 문제 마스터 & 과목별 통계
# -------------------------------------
problems_res = supabase.table("problems_master").select("*").execute()
problems = problems_res.data or []
problem_df = pd.DataFrame(problems)

if len(problem_df) > 0:
    problem_df = problem_df.set_index("id")

    wrong_ids = [x["problem_id"] for x in wrong]
    history_ids = [x["problem_id"] for x in history]

    if len(history_ids) > 0:
        df = problem_df.loc[history_ids].copy()
        df["is_wrong"] = df.index.isin(wrong_ids)

        subject_stats = df.groupby("subject")["is_wrong"].mean().reset_index()
        subject_stats["accuracy"] = 100 - subject_stats["is_wrong"] * 100

        st.subheader("📘 과목별 정답률")
        st.plotly_chart(
            px.bar(subject_stats, x="subject", y="accuracy", title="과목별 정확도 (%)"),
            use_container_width=True
        )
    else:
        st.info("풀이 기록이 아직 없습니다.")
else:
    st.info("문제 마스터 데이터가 없습니다.")

# -------------------------------------
# 4) AI 맞춤형 학습 조언
# -------------------------------------
if st.button("🧠 AI가 나의 학습 전략 생성하기"):
    feedback = ai_coach_feedback(history, wrong)
    st.markdown("### 🧠 AI 학습 코치의 조언")
    st.write(feedback)
