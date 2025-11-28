from core.db import supabase, fetch_one, insert
import bcrypt

def signup(email: str, password: str):
    # 이메일 중복 체크
    exist = fetch_one("profiles", "email", email)
    if exist:
        return None, "이미 존재하는 이메일입니다."

    # 비밀번호 해시
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # 프로필 생성
    insert("profiles", {
        "email": email,
        "password": hashed
    })

    return True, None


def login(email: str, password: str):
    user = fetch_one("profiles", "email", email)
    if not user:
        return None, "존재하지 않는 이메일입니다."

    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return None, "비밀번호가 올바르지 않습니다."

    return user, None
