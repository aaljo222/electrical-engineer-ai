from core.db import get_supabase
from werkzeug.security import generate_password_hash, check_password_hash

supabase = get_supabase()


def signup(email: str, password: str):
    # 이메일 중복 체크
    exist = supabase.table("profiles").select("*").eq("email", email).execute()
    if exist.data:
        return None, "이미 존재하는 이메일입니다."

    hashed = generate_password_hash(password)

    res = supabase.table("profiles").insert({
        "email": email,
        "password": hashed
    }).execute()

    return True, None


def login(email: str, password: str):
    res = supabase.table("profiles").select("*").eq("email", email).execute()

    if not res.data:
        return None

    row = res.data[0]

    if not check_password_hash(row["password"], password):
        return None

    return row
