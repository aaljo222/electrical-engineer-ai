import anthropic
import base64
import json
import re
from PIL import Image
import io
import streamlit as st

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_KEY"])

def analyze_image(image_bytes):
    b64 = base64.b64encode(image_bytes).decode()

    prompt = """
아래 이미지에 있는 전기기사 문제를 JSON만 출력하세요:

{
 "problem": "",
 "formula": ""
}
"""

    res = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": b64
                    }
                }
            ]
        }]
    )

    text = res.content[0].text.strip()

    try:
        return json.loads(text)
    except:
        try:
            block = re.search(r"\{.*?\}", text, re.S).group()
            return json.loads(block)
        except:
            return {"problem": "", "formula": ""}
