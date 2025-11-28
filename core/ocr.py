import anthropic
import os
import base64

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

MODEL = "claude-3-5-haiku-20241022"   # OCR 최적 모델

def analyze_image(img_bytes):
    """
    이미지에서 문제와 공식을 OCR 리딩해서 추출
    """
    image_base64 = base64.b64encode(img_bytes).decode()

    prompt = """
당신은 전기기사 문제 OCR 전문가입니다.
이미지에서 문제와 공식을 정확하게 추출하세요.

출력 형식:
문제: ...
공식: ...
"""

    res = client.messages.create(
        model=MODEL,
        max_tokens=800,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_base64
                    }
                }
            ]
        }]
    )

    text = res.content[0].text

    problem = ""
    formula = ""

    for line in text.split("\n"):
        if line.startswith("문제:"):
            problem = line.replace("문제:", "").strip()
        if line.startswith("공식:"):
            formula = line.replace("공식:", "").strip()

    return problem, formula
