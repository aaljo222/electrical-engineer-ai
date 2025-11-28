import hashlib
from core.db import supabase_query

def hash_pw(pw: str):
    return hashlib.sha256(pw.encode()).hexdigest()

def signup(email, password):
    h = hash_pw(password)

    # 이메일 중복 체크
    exists = supabase_query("select * from users where email = %s", (email,))
    if exists:
        return None, "이미 존재하는 이메일입니다."

    supabase_query(
        "insert into users (email, password) values (%s, %s)",
        (email, h)
    )
    return {"email": email}, None

def login(email, password):
    h = hash_pw(password)

    user = supabase_query(
        "select id, email from users where email = %s and password = %s",
        (email, h)
    )

    return user[0] if user else None
