
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "core"))


import streamlit as st
import plotly.express as px
import pandas as pd
from core.db import supabase

st.title("📊 기출문제 연도/유형 통계")

# 데이터 로드
problems = supabase.table("problems_master").select("*").execute().data
df = pd.DataFrame(problems)

# 연도별 문제 수
st.subheader("📌 연도별 출제 문항 수")
st.plotly_chart(
    px.histogram(df, x="year", title="연도별 문제 수"),
    use_container_width=True
)

# 과목별 문제 분포
st.subheader("📌 과목별 문제 분포")
st.plotly_chart(
    px.histogram(df, x="subject", title="과목별 문제수"),
    use_container_width=True
)

# 세션 분석
st.subheader("📌 회차별 출제 경향")
st.plotly_chart(
    px.histogram(df, x="session", color="subject"),
    use_container_width=True
)
