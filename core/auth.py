from core.db import fetch_one, execute
import bcrypt

def signup(email: str, password: str):
    # 이메일 중복 체크
    exist = fetch_one("SELECT * FROM profiles WHERE email=%s", (email,))
    if exist:
        return None, "이미 존재하는 이메일입니다."

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    execute(
        "INSERT INTO profiles(email, password) VALUES(%s, %s)",
        (email, hashed)
    )
    return True, None


def login(email: str, password: str):
    user = fetch_one("SELECT * FROM profiles WHERE email=%s", (email,))
    if not user:
        return None, "존재하지 않는 이메일입니다."

    hashed = user["password"]

    if bcrypt.checkpw(password.encode(), hashed.encode()):
        return user, None
    else:
        return None, "비밀번호가 일치하지 않습니다."


def logout():
    return True
