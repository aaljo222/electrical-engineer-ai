from core.db import fetch_one, insert
import bcrypt


def signup(email: str, password: str):
    # 이메일 중복 체크
    exist = fetch_one("profiles", "email", email)

    if exist is not None:
        return None, "이미 존재하는 이메일입니다."

    # 비밀번호 해싱
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    data = {
        "email": email,
        "password": hashed
    }

    insert("profiles", data)
    return True, None


def login(email: str, password: str):
    user = fetch_one("profiles", "email", email)

    if user is None:
        return None, "존재하지 않는 이메일입니다."

    hashed = user["password"].encode("utf-8")

    if not bcrypt.checkpw(password.encode("utf-8"), hashed):
        return None, "비밀번호가 일치하지 않습니다."

    return user, None
