import base64
import json
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def analyze_circuit_image(image_bytes):
    img_b64 = base64.b64encode(image_bytes).decode()

    prompt = """
아래 회로도 이미지를 분석하세요.

출력 형식(JSON):
{
 "elements": [
    {"type":"resistor", "value":"R1", "between":"A-B"},
    {"type":"inductor", "value":"L", "between":"B-C"},
    ...
 ],
 "nodes": ["A","B","C"],
 "topology": "series" 또는 "parallel" 또는 "T형" 또는 "π형",
 "equivalent_formula": "Z_eq = ...",
 "problem_summary": "이 회로의 목적 요약"
}
"""

    resp = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": img_b64
                    }
                }
            ]
        }]
    )

    return json.loads(resp.content[0].text)
