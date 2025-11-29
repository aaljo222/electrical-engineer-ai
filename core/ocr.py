import easyocr

reader = easyocr.Reader(['ko', 'en'])  # 한글 + 영어 지원

def extract_text_from_image(uploaded_file):
    """
    Streamlit 업로드 파일을 EasyOCR로 텍스트로 변환
    """
    image_bytes = uploaded_file.read()
    result = reader.readtext(image_bytes, detail=0)

    text = "\n".join(result)
    return text
