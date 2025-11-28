def ai_coach_feedback(history, wrong):
    prompt = f"""
당신은 전기기사 전문 학습 코치입니다.
다음은 학습자의 기록입니다.

전체 풀이 수: {len(history)}
오답 수: {len(wrong)}

이 사용자가 앞으로 어떤 학습 전략을 취해야 하는지,
약한 과목, 개선 포인트, 하루 루틴을 제안해 주세요.

출력 형식:
1) 현재 실력 진단
2) 약한 영역 분석
3) 다음 7일 학습 계획
4) 자주 틀리는 문제 패턴
5) 추천 기출 유형
    """

    resp = client.messages.create(
        model="claude-3-sonnet",
        messages=[{"role":"user","content":prompt}],
        max_tokens=1200
    )

    return resp.content[0].text
