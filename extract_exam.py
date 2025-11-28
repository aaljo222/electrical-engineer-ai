import fitz  # PyMuPDF
import re
import json
import base64
from PIL import Image
from io import BytesIO

# ------------------------
# 문제 패턴 정규식
# ------------------------
QUESTION_PATTERN = re.compile(r"(\d+)\.\s*(.*)")
CHOICE_PATTERN = re.compile(r"^[①②③④]|^\(\d\)")
ANSWER_PATTERN = re.compile(r"정답\s*[:：]\s*([①②③④]|\d)")


# ①②③④ → 숫자로 변경
choice_map = {"①":1, "②":2, "③":3, "④":4}


def extract_images(page, qid):
    images = []
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base = page.parent.extract_image(xref)
        img_bytes = base["image"]

        output = base64.b64encode(img_bytes).decode()

        images.append({
            "qid": qid,
            "image_base64": output
        })

    return images


def extract_exam(pdf_path):
    doc = fitz.open(pdf_path)

    problems = []
    all_images = []

    current_qid = None
    current_text = ""
    current_choices = []

    for page_number, page in enumerate(doc):
        text = page.get_text()

        lines = text.split("\n")

        for line in lines:

            # 문제 번호 찾기
            q_match = QUESTION_PATTERN.match(line)
            if q_match:
                # 이전 문제 저장
                if current_qid:
                    problems.append({
                        "id": current_qid,
                        "question": current_text.strip(),
                        "choices": current_choices,
                        "answer": None,
                        "images": []  # 나중에 매칭
                    })

                current_qid = int(q_match.group(1))
                current_text = q_match.group(2)
                current_choices = []
                continue

            # 보기
            if CHOICE_PATTERN.match(line.strip()):
                current_choices.append(line.strip())
                continue

            # 정답
            ans_match = ANSWER_PATTERN.search(line)
            if ans_match:
                ans_val = ans_match.group(1)
                if ans_val in choice_map:
                    ans_val = choice_map[ans_val]
                else:
                    ans_val = int(ans_val)

                # 저장
                if current_qid:
                    problems[-1]["answer"] = ans_val
                continue

            # 문제 내용 이어 붙이기
            if current_qid:
                current_text += " " + line.strip()

        # 이미지 추출
        if current_qid:
            extracted = extract_images(page, current_qid)
            all_images.extend(extracted)

    # 이미지 매칭
    for p in problems:
        p["images"] = [img["image_base64"] for img in all_images if img["qid"] == p["id"]]

    return problems


if __name__ == "__main__":
    pdf_file = "전기기사20220424(교사용).pdf"

    results = extract_exam(pdf_file)

    with open("exam_output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print("완료! exam_output.json 생성됨.")
