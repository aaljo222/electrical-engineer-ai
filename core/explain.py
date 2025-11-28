import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

MODEL = "claude-3-5-sonnet-latest"

def generate_explanation(problem, formula, related):
    context = ""
    for p in related:
        context += f"""
[기출 {p['year']}년 {p['session']}회 Q{p['id']}]
문제: {p['question']}
정답: {p['answer']}
공식: {p['formula']}
"""

    prompt = f"""
당신은 전기기사 전문 강사입니다.

문제:
{problem}

공식:
{formula}

참고 기출문제:
{context}

다음 형식으로 설명하세요:
1) 문제 핵심  
2) 개념 설명  
3) 공식 유도  
4) 단계별 풀이  
5) 암기 팁  
"""

    res = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return res.content[0].text


def ai_coach_feedback(history, wrong):
    total = len(history)
    wrong_cnt = len(wrong)
    acc = round((total - wrong_cnt) / total * 100, 1) if total else 0

    prompt = f"""
당신은 전기기사 AI 학습 코치입니다.

사용자 통계:
- 전체 풀이 수: {total}
- 오답 수: {wrong_cnt}
- 정답률: {acc} %

옵션:
1) 현재 실력 진단
2) 취약 단원 분석
3) 앞으로의 학습 전략
4) 7일 학습 계획
5) 에너지/컨디션 조절 팁
"""

    res = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt}]
)


    return res.content[0].text
