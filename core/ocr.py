import base64
from anthropic import Anthropic
import os

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def analyze_image(image_bytes):
    img_b64 = base64.b64encode(image_bytes).decode()

    prompt = """
전기기사 시험 문제 이미지입니다.

아래 JSON 형식으로 출력하세요:

{
 "problem": "...",
 "formula": "..."
}
JSON 외 설명 금지.
"""
    response = client.messages.create(
        model="claude-3-haiku-20240307",
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
                            "data": img_b64
                        }
                    }
                ]
            }
        ]
    )

    import json
    import re

    raw = response.content[0].text

    try:
        result = json.loads(raw)
        return result.get("problem", ""), result.get("formula", "")
    except:
        match = re.search(r"\{.*?\}", raw, re.S)
        if match:
            result = json.loads(match.group())
            return result.get("problem", ""), result.get("formula", "")
        return "", ""
