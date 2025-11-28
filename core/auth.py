import hashlib
from core.db import fetch_one, execute


def hash_pw(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def signup(email, password):
    # 이메일 중복 확인
    exist = fetch_one("SELECT * FROM profiles WHERE email=%s", (email,))
    if exist:
        return None, "이미 존재하는 이메일입니다."

    h = hash_pw(password)

    execute(
        "INSERT INTO profiles (email, password) VALUES (%s, %s)",
        (email, h)
    )
    return True, None


def login(email, password):
    h = hash_pw(password)
    user = fetch_one(
        "SELECT id, email FROM profiles WHERE email=%s AND password=%s",
        (email, h)
    )
    return user
