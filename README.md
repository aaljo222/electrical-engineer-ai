# 전기기사 공식 AI 설명 생성기 (Streamlit)

Claude AI를 활용한 전기기사 시험 공식 설명 서비스

## 🎈 Streamlit의 장점

- ✅ **완전 무료 배포** (Streamlit Community Cloud)
- ✅ **UI 자동 생성** (HTML/CSS 불필요)
- ✅ **GitHub 연동 자동**
- ✅ **실시간 리로드**
- ✅ **Python만 알면 OK**

---

## 🚀 Streamlit Cloud 배포 (2분!)

### 1. GitHub에 업로드

```bash
cd electrical_engineer_streamlit
git init
git add .
git commit -m "Initial commit"

# GitHub 새 저장소 생성 후
git remote add origin https://github.com/your-username/electrical-ai.git
git push -u origin main
```

### 2. Streamlit Cloud 배포

1. https://streamlit.io/cloud 접속
2. "Sign up" → GitHub 계정 연결
3. "New app" 클릭
4. 저장소 선택:
   - Repository: `your-username/electrical-ai`
   - Branch: `main`
   - Main file: `app.py`
5. **Advanced settings** → Secrets 추가:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-api03-..."
   ```
6. "Deploy!" 클릭

**2분 후 완성!** 🎉

배포 URL: `https://your-app.streamlit.app`

---

## 🔧 로컬 테스트

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. Secrets 설정

`.streamlit/secrets.toml` 파일 수정:
```toml
ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

### 3. 실행

```bash
streamlit run app.py
```

브라우저 자동 오픈: `http://localhost:8501`

---

## 📁 프로젝트 구조

```
electrical_engineer_streamlit/
├── app.py                    # 메인 Streamlit 앱
├── requirements.txt          # Python 패키지
├── .streamlit/
│   ├── config.toml          # Streamlit 설정
│   └── secrets.toml         # API 키 (로컬용)
└── .gitignore
```

---

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

## ⚙️ Streamlit Cloud 설정

### Secrets 추가 방법

배포 후:
1. 앱 대시보드 → Settings
2. Secrets 섹션
3. 추가:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-api03-..."
   ```
4. Save

### 재배포

코드 수정 후:
```bash
git add .
git commit -m "Update"
git push
```

자동으로 재배포됨!

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

## 📊 vs 다른 방식

| 항목 | Vercel | Railway | Streamlit |
|------|--------|---------|-----------|
| 설정 | 복잡 | 중간 | **매우 쉬움** |
| 비용 | 무료 | $5/월 | **무료** |
| Python | 까다로움 | 쉬움 | **매우 쉬움** |
| UI | 직접 코딩 | 직접 코딩 | **자동** |
| 배포 | 5분 | 3분 | **2분** |

---

## 🐛 문제 해결

### API 키 오류

Streamlit Cloud → Settings → Secrets 확인

### 앱이 느림

무료 플랜은 슬립 모드:
- 첫 접속 시 깨어남 (5-10초)
- 이후 정상 속도

### 재배포 안됨

```bash
# 강제 재배포
git commit --allow-empty -m "Redeploy"
git push
```

---

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

## 📞 지원

- Streamlit 문서: https://docs.streamlit.io
- 커뮤니티: https://discuss.streamlit.io

---

**Streamlit이 가장 쉽습니다!** 🚀
