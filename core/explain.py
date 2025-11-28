import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def make_explanation(problem_text: str):
    prompt = f"""
    전기기사 문제 해설을 다음 형식으로 만들어줘:

    문제: {problem_text}

    1) 사용 공식
    2) 단계별 풀이
    3) 최종 답
    """

    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return res["choices"][0]["message"]["content"]
