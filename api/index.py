from flask import Flask, request, jsonify
from datetime import datetime
import anthropic
import os
import hashlib
import json

app = Flask(__name__)

# API 키 (Vercel 환경변수에서 가져옴)
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# 간단한 인메모리 캐시
cache = {}

def generate_hash(problem_text, formula):
    content = f"{problem_text}||{formula}"
    return hashlib.md5(content.encode()).hexdigest()

def generate_explanation(problem_text, formula):
    """Claude API로 공식 설명 생성"""
    
    if not ANTHROPIC_API_KEY:
        return None
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    prompt = f"""전기기사 시험 문제를 쉽게 설명해주세요.

문제: {problem_text}
공식: {formula}

다음 형식으로 단계별 설명을 작성하세요:

## 1. 문제 이해
[문제를 쉽게 풀어서 설명]

## 2. 필요한 개념
[관련 개념 설명]

## 3. 공식 유도
[공식을 어떻게 유도하는지 단계별로]

## 4. 예제 풀이
[구체적인 숫자를 넣어서 예제 문제 풀이]

## 5. 암기 팁
[공식을 쉽게 외우는 방법]

한글로 친절하게 설명해주세요. 마크다운 형식으로 작성하되, 수식은 LaTeX 없이 일반 텍스트로 표현하세요.
"""
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
        
    except Exception as e:
        print(f"Claude API 오류: {e}")
        return None

@app.route('/api/generate', methods=['POST'])
def generate():
    """설명 생성 API"""
    try:
        data = request.get_json()
        problem_text = data.get('problem', '')
        formula = data.get('formula', '')
        
        if not problem_text or not formula:
            return jsonify({
                'success': False,
                'error': '문제와 공식을 모두 입력해주세요.'
            }), 400
        
        # 해시 생성
        content_hash = generate_hash(problem_text, formula)
        
        # 캐시 확인
        if content_hash in cache:
            return jsonify({
                'success': True,
                'cached': True,
                'explanation': cache[content_hash]['explanation'],
                'created_at': cache[content_hash]['created_at']
            })
        
        # 설명 생성
        explanation = generate_explanation(problem_text, formula)
        
        if not explanation:
            return jsonify({
                'success': False,
                'error': 'API 키가 설정되지 않았거나 생성에 실패했습니다.'
            }), 500
        
        # 캐시 저장
        cache[content_hash] = {
            'problem': problem_text,
            'formula': formula,
            'explanation': explanation,
            'created_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'cached': False,
            'explanation': explanation,
            'created_at': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """헬스체크"""
    return jsonify({
        'success': True,
        'message': 'API is running',
        'api_key_set': bool(ANTHROPIC_API_KEY)
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """정적 파일 서빙"""
    return app.send_static_file('index.html')

# Vercel용 핸들러 - 이게 핵심!
def handler(environ, start_response):
    return app(environ, start_response)