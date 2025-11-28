import pytesseract
from PIL import Image
import tempfile

def analyze_image(uploaded_file):
    """이미지 → 텍스트 OCR"""
    try:
        # Streamlit의 UploadedFile을 실제 이미지로 변환
        img = Image.open(uploaded_file)

        # OCR 수행
        text = pytesseract.image_to_string(img, lang="kor+eng")

        # 불필요한 공백 제거
        text = text.strip()

        return text if text else "OCR 실패: 텍스트를 읽을 수 없습니다."

    except Exception as e:
        return f"OCR 오류: {e}"
