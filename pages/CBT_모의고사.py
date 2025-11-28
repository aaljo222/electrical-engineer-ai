import streamlit as st
import random
from core.db import supabase
from core.auth import check_login


st.set_page_config(layout="wide")
st.title("📝 전기기사 CBT 모의고사")

user = check_login()

# -------------------------------
# 1) 문제 100개 랜덤 로드
# -------------------------------
problems = (
    supabase.table("problems_master")
    .select("*")
    .order("RANDOM()", desc=False)
    .limit(100)
    .execute()
).data

if "answers" not in st.session_state:
    st.session_state.answers = {}

# -------------------------------
# 2) 문제 출력
# -------------------------------
for idx, p in enumerate(problems):
    st.markdown(f"### {idx + 1}. {p['question']}")

    for i, choice in enumerate(p["choices"]):
        key = f"q{idx}"
        st.radio(
            label="",
            options=[f"{i + 1}. {choice}"],
            key=f"{key}-{i}",
            index=None
        )

st.markdown("---")

# -------------------------------
# 3) 제출 버튼
# -------------------------------
if st.button("📌 시험 제출하기", type="primary"):
    correct = 0
    wrong_list = []

    for idx, p in enumerate(problems):
        correct_ans = p["answer"]
        selected = None

        # Find selected choice
        for i in range(len(p["choices"])):
            key = f"q{idx}-{i}"
            if st.session_state.get(key):
                selected = i + 1

        if selected == correct_ans:
            correct += 1
        else:
            wrong_list.append({
                "problem_id": p["id"],
                "user_answer": selected
            })

    st.success(f"🎉 총점: {correct} / 100")

    # 오답 저장
    for w in wrong_list:
        supabase.table("user_wrongbook").insert({
            "user_id": user.id,
            "problem_id": w["problem_id"],
            "user_answer": w["user_answer"]
        }).execute()

    st.info(f"❌ 오답 {len(wrong_list)}개가 오답노트에 저장되었습니다.")
