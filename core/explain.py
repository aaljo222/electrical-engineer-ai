import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-sonnet-4-5-20250514"

# ---------------------------
# 1) AI 기반 채점
# ---------------------------
def grade_answer(correct_answer, user_answer):
    prompt = f"""
당신은 전기기사 전문 채점관입니다.

정답: {correct_answer}
사용자 답: {user_answer}

두 값이 의미적으로 같으면 1, 틀리면 0을 출력하세요.
설명 없이 숫자만 출력하세요.
"""
    res = client.messages.create(
        model=MODEL,
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )

    return res.content[0].text.strip() == "1"


# ---------------------------
# 2) AI 설명 생성
# ---------------------------
def make_explanation(problem_text, formula):
    prompt = f"""
문제: {problem_text}
공식: {formula}

전기기사 문제를 단계적으로 설명하세요.
"""

    res = client.messages.create(
        model=MODEL,
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.content[0].text
