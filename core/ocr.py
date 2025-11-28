import anthropic
import os
from PIL import Image
import base64
import io

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

MODEL = "claude-3-5-haiku-latest"   # OCR 최적

def analyze_image(img_bytes):
    """
    이미지에서 텍스트(문제·공식)를 추출하는 함수
    """
    image_base64 = base64.b64encode(img_bytes).decode("utf-8")

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
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64,
                        },
                    },
                ],
            }
        ],
    )

    text = res.content[0].text

    # 간단 파싱
    problem = ""
    formula = ""

    for line in text.split("\n"):
        if line.startswith("문제:"):
            problem = line.replace("문제:", "").strip()
        elif line.startswith("공식:"):
            formula = line.replace("공식:", "").strip()

    return problem, formula
