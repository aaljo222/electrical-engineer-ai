import streamlit as st
import pandas as pd
from core.auth import check_login
from core.db import get_supabase

st.set_page_config(page_title="학습기록", layout="wide")
st.title("📒 학습 기록")

user = check_login()
supabase = get_supabase()

history = (
    supabase.table("user_history")
    .select("*")
    .eq("user_id", user["id"])
    .execute()
).data

if not history:
    st.info("아직 풀이 기록이 없습니다.")
    st.stop()

df = pd.DataFrame(history)
st.dataframe(df, use_container_width=True)
