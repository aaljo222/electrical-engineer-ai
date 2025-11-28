import streamlit as st
from core.auth import check_login
from core.db import get_supabase

st.set_page_config(page_title="오답노트", layout="wide")
st.title("❌ 오답노트")

user = check_login()
supabase = get_supabase()

wrong_list = (
    supabase.table("user_wrongbook")
    .select("problem_id")
    .eq("user_id", user["id"])
    .execute()
).data

if not wrong_list:
    st.info("오답이 없습니다!")
    st.stop()

problem_ids = [x["problem_id"] for x in wrong_list]

problems = (
    supabase.table("problems_master")
    .select("*")
    .in_("id", problem_ids)
    .execute()
).data

for p in problems:
    st.markdown(f"### Q{p['id']} - {p['subject']}")
    st.write(p["question"])
    st.info(f"정답: {p['answer']}")
    st.write("---")
