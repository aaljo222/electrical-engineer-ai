import fitz
import re
import json
import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def extract_raw_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def split_questions(raw_text):
    pattern = r"(?:문제\s*\d+\.)"
    parts = re.split(pattern, raw_text)
    nums = re.findall(pattern, raw_text)

    questions = []
    for idx, body in enumerate(parts[1:], start=1):
        qnum = re.findall(r"\d+", nums[idx-1])[0]
        questions.append((int(qnum), body.strip()))
    return questions


def refine_with_claude(qnum, body):
    prompt = f"""
너는 전기기사 기출 문제 정제기이다.

다음 문제 텍스트를 JSON으로 정제해라:

문제번호: {qnum}
본문:
{body}

출력 예시:
{{
 "id": 번호,
 "question": "...문제 내용...",
 "choices": ["A ...", "B ...", "C ...", "D ..."],
 "answer": "정답",
 "formula": "관련 공식"
}}
"""

    resp = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(resp.content[0].text)


def extract_pdf_to_json(pdf_path, output_path="problems.json"):
    raw = extract_raw_text(pdf_path)
    qs = split_questions(raw)

    results = []
    for qnum, body in qs:
        print("정제 중:", qnum)
        data = refine_with_claude(qnum, body)
        results.append(data)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print("완료:", output_path)
