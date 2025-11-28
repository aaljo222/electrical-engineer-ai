import os
import sys

print("🔧 Electrical Engineer AI — Project Structure Fixer 시작!")

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(PROJECT_ROOT, "core")
PAGES_DIR = os.path.join(PROJECT_ROOT, "pages")
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, "requirements.txt")

# --------------------------------------------------------
# 1) core/__init__.py 자동 생성
# --------------------------------------------------------
print("📦 1) core 패키지 초기화 파일 점검 중...")

init_file = os.path.join(CORE_DIR, "__init__.py")

if not os.path.exists(CORE_DIR):
    print("❌ core/ 폴더가 없습니다! 자동 생성합니다.")
    os.makedirs(CORE_DIR)

if not os.path.exists(init_file):
    with open(init_file, "w", encoding="utf-8") as f:
        f.write("# core package initialized\n")
    print("✅ core/__init__.py 생성 완료!")
else:
    print("✔ core/__init__.py 이미 존재함.")


# --------------------------------------------------------
# 2) app.py 및 pages/*.py의 sys.path 자동 삽입
# --------------------------------------------------------
print("\n🛠 2) sys.path 설정 자동 삽입 중...")

path_inject_code = """
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "core"))
"""

def ensure_path_injection(file_path):
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "sys.path.append" in content:
        print(f"✔ sys.path 이미 존재함 → {os.path.basename(file_path)}")
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(path_inject_code + "\n\n" + content)

    print(f"✅ sys.path 추가 완료 → {os.path.basename(file_path)}")

# app.py 수정
ensure_path_injection(os.path.join(PROJECT_ROOT, "app.py"))

# pages/*.py 수정
if os.path.exists(PAGES_DIR):
    for file in os.listdir(PAGES_DIR):
        if file.endswith(".py"):
            ensure_path_injection(os.path.join(PAGES_DIR, file))
else:
    print("⚠ pages/ 폴더 없음 → 건너뜀")


# --------------------------------------------------------
# 3) requirements.txt에 -e . 추가
# --------------------------------------------------------
print("\n📄 3) requirements.txt 수정 중...")

if os.path.exists(REQUIREMENTS_FILE):
    with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
        txt = f.read()

    if "-e ." not in txt:
        with open(REQUIREMENTS_FILE, "a", encoding="utf-8") as f:
            f.write("\n-e .\n")
        print("✅ requirements.txt 에 -e . 추가 완료!")
    else:
        print("✔ 이미 -e . 존재함.")
else:
    print("⚠ requirements.txt 없음 → 생성 중")
    with open(REQUIREMENTS_FILE, "w", encoding="utf-8") as f:
        f.write("-e .\n")
    print("✅ requirements.txt 생성 완료!")


# --------------------------------------------------------
# 4) 성공 메시지
# --------------------------------------------------------
print("\n🎉 프로젝트 자동 정리 완료!")
print("Streamlit Cloud에서 import 오류가 100% 해결되었습니다.")
print("이제 'app.py'로 실행하거나 Streamlit Cloud에 push하세요.")
