import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

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

참고할 기출문제:
{context}

다음 형식으로 자세히 설명하세요:
1) 문제 핵심  
2) 개념 설명  
3) 공식 유도  
4) 단계별 풀이  
5) 암기 팁  
"""

    res = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return res.content[0].text

import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def ai_coach_feedback(history, wrong):
    total = len(history)
    wrong_count = len(wrong)

    prompt = f"""
당신은 전기기사 전문 AI 학습 코치입니다.

사용자 데이터:
- 전체 풀이 수: {total}
- 오답 수: {wrong_count}
- 정답률: {round((total - wrong_count) / total * 100, 1) if total else 0} %

오답 목록과 풀이 기록을 분석하여 아래 형식으로 설명하세요:

1) 학습자 현재 실력 분석  
2) 자주 틀리는 개념 또는 단원  
3) 앞으로 집중해야 할 학습 전략  
4) 다음 7일 학습 스케줄  
5) 에너지 관리 팁  
"""

    res = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return res.content[0].text
