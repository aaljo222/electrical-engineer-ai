import streamlit as st
from core.db import supabase_query
from core.auth import check_login

st.title("📕 오답노트")

user = check_login()

wrongs = supabase_query("user_wrongbook", {"user_id": user.id})

if not wrongs:
    st.info("아직 오답이 없습니다.")
    st.stop()

for item in wrongs:
    with st.expander(f"문제 ID {item['problem_id']}"):
        st.write("❌ 사용자 답:", item["user_answer"])

        if st.button("🔖 북마크", key=f"bm{item['id']}"):
            supabase_query("user_wrongbook", {"id": item["id"]}, update={"is_bookmarked": True})
            st.rerun()