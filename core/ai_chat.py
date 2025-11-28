def answer_question(query):
    prompt = f"""
당신은 전기기사 전문 강사입니다.
다음 질문에 명확하고 쉬운 설명을 해주세요:

질문: {query}

출력 형식:
1) 핵심 요약
2) 상세 개념 설명
3) 공식
4) 기출 문제 예시
5) 응용 문제
"""
    resp = client.messages.create(
        model="claude-3-sonnet",
        messages=[{"role":"user","content":prompt}],
        max_tokens=1500
    )

    return resp.content[0].text
