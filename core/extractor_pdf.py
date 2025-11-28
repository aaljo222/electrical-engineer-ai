import fitz
import base64
import json
import re

def extract_pdf_to_json(path):
    doc = fitz.open(path)
    problems = []
    current = {"question_no": None, "question": "", "choices": []}

    for page in doc:
        text = page.get_text()
        lines = text.split("\n")

        for line in lines:
            # 문제 번호 탐지
            m = re.match(r"(\d+)\.\s*(.*)", line)
            if m:
                if current["question_no"]:
                    problems.append(current)
                current = {
                    "question_no": int(m.group(1)),
                    "question": m.group(2),
                    "choices": []
                }
            elif line.strip().startswith("("):
                current["choices"].append(line.strip())
            else:
                current["question"] += " " + line.strip()

    problems.append(current)

    return problems
