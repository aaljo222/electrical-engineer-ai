# auth_db.py
from supabase_rest import db_select, db_insert
import uuid
from datetime import datetime

# ------------------------------
# 회원가입
# ------------------------------
def signup(email, password):
    users = db_select("users", {"email": f"eq.{email}"})

    if users:
        return None, "이미 존재하는 이메일입니다."

    new_user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password": password,
        "created_at": datetime.utcnow().isoformat()
    }

    inserted = db_insert("users", new_user)
    return inserted, None

# ------------------------------
# 로그인
# ------------------------------
def login(email, password):
    result = db_select(
        "users",
        {
            "email": f"eq.{email}",
            "password": f"eq.{password}"
        },
        limit=1
    )

    if result:
        return result[0]
    return None

def logout():
    pass  # Streamlit session 자체가 맡아서 처리함

# ------------------------------
# 사용자 ID로 조회
# ------------------------------
def get_user(user_id):
    result = db_select("users", {"id": f"eq.{user_id}"}, limit=1)
    if result:
        return result[0]
    return None

# ------------------------------
# 기록 저장
# ------------------------------
def save_history(user_id, problem, formula, explanation):
    data = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "problem": problem,
        "formula": formula,
        "explanation": explanation,
        "created_at": datetime.utcnow().isoformat()
    }
    return db_insert("history", data)

# ------------------------------
# 기록 조회
# ------------------------------
def get_history(user_id):
    return db_select("history", {"user_id": f"eq.{user_id}"})
