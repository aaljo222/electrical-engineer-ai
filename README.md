# 전기기사 공식 AI 설명 생성기 (Streamlit)

Claude AI를 활용한 전기기사 시험 공식 설명 서비스


### 1. GitHub에 업로드

```bash
cd electrical_engineer_streamlit
git init
git add .
git commit -m "Initial commit"



## 🎯 주요 기능

### 1. 문제 입력
- 텍스트 영역으로 문제 입력
- 공식 입력 필드

### 2. 예시 문제
- 사이드바에 3개 예시
- 클릭하면 자동 입력

### 3. AI 설명 생성
- Claude API 호출
- 10-30초 소요
- 마크다운 형식으로 표시

### 4. 캐싱
- 동일 문제는 즉시 반환
- 세션 상태로 관리

### 5. 다운로드
- 텍스트 파일로 다운로드 가능

---


## 🎨 커스터마이징

### 색상 변경

`.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#2563eb"        # 버튼 색상
backgroundColor = "#ffffff"      # 배경색
secondaryBackgroundColor = "#f1f5f9"  # 카드 배경
textColor = "#1e293b"           # 텍스트 색상
```

### 레이아웃 변경

`app.py`:
```python
st.set_page_config(
    page_title="당신의 제목",
    page_icon="⚡",
    layout="wide"  # 또는 "centered"
)
```

---

## 💰 비용

### Streamlit Community Cloud
- **완전 무료!**
- 무제한 앱
- 1GB RAM
- 1 CPU
- 충분합니다!

### Claude API
- 1회 요청: ~$0.024 (30원)
- 월 1,000회: ~$24 (3만원)

**총 비용: Claude API만 발생**

---


## 🐛 문제 해결

### API 키 오류

Streamlit Cloud → Settings → Secrets 확인



## 🎁 보너스 기능

### 추가할 수 있는 것들

1. **파일 업로드**
   ```python
   uploaded_file = st.file_uploader("이미지 업로드")
   ```

2. **차트 표시**
   ```python
   st.line_chart(data)
   ```

3. **데이터프레임**
   ```python
   st.dataframe(df)
   ```

4. **여러 페이지**
   ```python
   pages/
   ├── home.py
   ├── about.py
   └── settings.py
   ```

---

