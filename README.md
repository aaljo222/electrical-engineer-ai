# 전기기사 공식 AI 설명 생성기 (Vercel 배포용)

Claude AI를 활용한 전기기사 시험 공식 설명 서비스

## 🚀 Vercel 배포 방법

### 1. GitHub 저장소 생성

```bash
# 프로젝트 폴더에서
git init
git add .
git commit -m "Initial commit"

# GitHub에 새 저장소 생성 후
git remote add origin https://github.com/your-username/electrical-engineer-ai.git
git push -u origin main
```

### 2. Vercel 배포

**방법 A: Vercel CLI (빠름)**

```bash
# Vercel CLI 설치
npm install -g vercel

# 로그인
vercel login

# 배포
vercel

# 환경변수 설정
vercel env add ANTHROPIC_API_KEY

# 프로덕션 배포
vercel --prod
```

**방법 B: Vercel 웹사이트 (쉬움)**

1. https://vercel.com 접속
2. GitHub 계정으로 로그인
3. "New Project" 클릭
4. GitHub 저장소 선택
5. 환경변수 설정:
   - Key: `ANTHROPIC_API_KEY`
   - Value: `sk-ant-api03-...` (당신의 API 키)
6. "Deploy" 클릭

**완료! 🎉**

배포 URL: `https://your-project.vercel.app`

---

## 📁 프로젝트 구조

```
electrical_engineer_vercel/
├── vercel.json          # Vercel 설정
├── requirements.txt     # Python 패키지
├── api/
│   └── index.py        # Serverless 함수 (Flask)
└── public/
    └── index.html      # 프론트엔드
```

---

## 🔧 로컬 테스트

### Flask 개발 서버로 테스트 (Vercel 환경 아님)

```bash
# 환경변수 설정
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# 패키지 설치
pip install -r requirements.txt

# 개발 서버 실행
cd api
python -m flask --app index run --port 5000
```

브라우저: `http://localhost:5000`

---

## ⚙️ 환경변수 설정

### Vercel Dashboard에서:

1. 프로젝트 → Settings → Environment Variables
2. 추가:
   ```
   ANTHROPIC_API_KEY = sk-ant-api03-...
   ```
3. Production, Preview, Development 모두 체크
4. Save

### CLI에서:

```bash
vercel env add ANTHROPIC_API_KEY production
# API 키 입력

vercel env add ANTHROPIC_API_KEY preview
# API 키 입력
```

---

## 🎯 특징

- ✅ **무료 배포** - Vercel 무료 플랜
- ✅ **빠른 응답** - Serverless 함수
- ✅ **자동 HTTPS** - 보안 연결
- ✅ **글로벌 CDN** - 빠른 로딩
- ✅ **자동 배포** - Git push만 하면 배포

---

## 📊 Vercel 무료 플랜 제한

- 함수 실행 시간: 10초
- 월 실행 횟수: 100,000회
- 대역폭: 100GB/월

**충분합니다!**
- 1회 요청 ~10초
- 월 10,000회 사용 가능
- 유료 회원 100명도 충분

---

## 🔄 업데이트 방법

```bash
# 코드 수정 후
git add .
git commit -m "Update"
git push

# 자동으로 Vercel에 배포됨!
```

---

## ⚠️ 주의사항

### Vercel 제약

1. **파일 저장 불가**
   - 캐시는 인메모리만 (재시작 시 삭제)
   - Redis/KV 사용 권장 (유료)

2. **함수 실행 시간 10초**
   - Claude API는 보통 5-10초
   - 충분하지만 복잡한 요청은 타임아웃 가능

3. **Cold Start**
   - 첫 요청은 느릴 수 있음 (2-3초)
   - 이후 요청은 빠름

---

## 🆙 업그레이드 옵션

### 캐시 추가 (Redis)

Vercel KV (Redis) 사용:

```bash
# Vercel KV 연결
vercel link

# KV 스토어 생성
vercel kv create
```

`api/index.py` 수정:
```python
from vercel_kv import KV

kv = KV()

# 캐시 저장
kv.set(content_hash, explanation)

# 캐시 조회
cached = kv.get(content_hash)
```

---

## 💰 비용

**Vercel 무료 플랜:**
- 배포: 무료
- 호스팅: 무료
- HTTPS: 무료
- 100,000회 함수 실행/월: 무료

**Claude API 비용:**
- 1회 요청: ~$0.024 (30원)
- 월 1,000회: ~$24 (3만원)

**총 비용: Claude API만 발생**

---

## 🎁 보너스 기능

### 커스텀 도메인

Vercel Dashboard:
1. Settings → Domains
2. 도메인 추가 (예: electrical-ai.com)
3. DNS 설정
4. 자동 HTTPS 적용

---

## 🐛 문제 해결

### API 키 오류
```bash
# Vercel 환경변수 확인
vercel env ls

# 재설정
vercel env rm ANTHROPIC_API_KEY
vercel env add ANTHROPIC_API_KEY
```

### 배포 실패
```bash
# 로그 확인
vercel logs

# 강제 재배포
vercel --force
```

---

## 📞 지원

문제가 있으면 Vercel Discord 또는 문서 참조:
- https://vercel.com/docs
- https://vercel.com/discord

---

**Happy Deploying! 🚀**
