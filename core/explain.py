# core/explain.py
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def grade_answer(problem_text: str, user_answer: str, correct_answer: str):
    prompt = f"""
너는 전기기사 시험 채점관이야.

문제:
{problem_text}

정답: {correct_answer}
사용자 답안: {user_answer}

JSON 형태로 출력:
{{
  "is_correct": true/false,
  "reason": "설명"
}}
"""

    resp = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    return json.loads(resp.content[0].text)

def make_explanation(problem_text: str, formula: str):
    prompt = f"""
문제:
{problem_text}

공식:
{formula}

전기기사 강사처럼 단계별 풀이 설명을 써줘.
"""

    resp = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.content[0].text
