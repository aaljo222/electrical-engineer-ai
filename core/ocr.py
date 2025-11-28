import anthropic
import os
import numpy as np
from core.db import supabase

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-3-haiku-20241022"

# OCR + 문제 검색
def analyze_image(image_bytes):
    """이미지 OCR + problems_master에서 유사 문제 검색"""

    # 1) OCR
    ocr_prompt = "다음 이미지에서 문제(문장만)를 정확히 추출하세요."
    res = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": ocr_prompt},
                {"type": "image", "source": {"type": "bytes", "bytes": image_bytes}}
            ]}
        ]
    )
    text = res.content[0].text.strip()

    # 2) problems_master에서 embedding 컬럼으로 검색
    emb = embed_text(text)
    matches = supabase.rpc("match_problems", {"query_embedding": emb, "match_count": 1}).execute()

    if len(matches.data) == 0:
        return None, None, None

    row = matches.data[0]
    return row["id"], row["question"], row["formula"]


def embed_text(text):
    """시멘틱 검색용 임베딩"""
    res = client.messages.create(
        model="claude-embedding-1",
        max_tokens=10,
        messages=[{"role": "user", "content": text}]
    )
    vec = res.content[0].embedding
    return vec
