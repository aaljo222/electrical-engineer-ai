import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def solve_problem(text):
    """
    이미지에서 추출된 텍스트(문제)를 입력받아
    Claude로 풀이/정답/난이도/출제 개념을 생성
    """
    prompt = f"""
다음 문제를 분석하고 아래 형식으로 답하세요.

문제:
{text}

아래 형식으로 출력:

1) 문제 요약:
2) 정답:
3) 상세 풀이 과정:
4) 사용된 개념:
5) 난이도 (상/중/하):
6) 유사 문제 출제 가능성 (%):
    """

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text
