import base64
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def analyze_image(file):
    image_bytes = file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    resp = client.messages.create(
        model="claude-3-5-sonnet-20240620",   # 🔥 최신 Vision 모델
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image", "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_image
                    }},
                    {"type": "text", "text": "이 이미지에서 문제 문장을 그대로 텍스트로 추출해줘. 수식은 LaTeX 그대로 유지해줘."}
                ]
            }
        ]
    )

    return resp.content[0].text.strip()
