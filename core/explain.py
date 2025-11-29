import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def solve_problem(text):
    """
    OCR로 추출된 문제 텍스트를 Claude로 보내
    정답 + 상세 풀이 + 사용된 개념을 생성하는 함수
    """

    prompt = f"""
너는 전기기사 문제 전문 AI다.

반드시 아래 구조로만 대답해:

정답: (숫자 또는 공식)

상세 풀이 과정:
(여기에 단계별 풀이 적기)

사용된 개념:
(여기에 전기 이론 개념 설명)

문제:
{text}
"""

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            }
        ]
    )

    return message.content[0].text
