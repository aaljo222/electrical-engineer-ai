from anthropic import Anthropic
import os

api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

def solve_problem(problem_text: str):
    """OCR된 문제 텍스트를 기반으로 풀이 생성"""

    prompt = f"""
다음은 전기기사 시험 문제입니다.
문제 텍스트:
