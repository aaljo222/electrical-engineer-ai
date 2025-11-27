from flask import Flask, render_template_string, request, jsonify
import anthropic
import os
import hashlib
import json
from datetime import datetime

app = Flask(__name__)

# API 키
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# 캐시
cache = {}

def generate_hash(problem_text, formula):
    content = f"{problem_text}||{formula}"
    return hashlib.md5(content.encode()).hexdigest()

def generate_explanation(problem_text, formula):
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

# HTML 템플릿 (인라인)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>전기기사 공식 AI 설명 생성기</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #1e293b;
            padding: 2rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header { text-align: center; color: white; margin-bottom: 3rem; }
        header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        main { background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 1.5rem; }
        label { display: block; margin-bottom: 0.5rem; font-weight: 600; }
        textarea, input { width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 1rem; font-family: inherit; }
        textarea { min-height: 120px; resize: vertical; }
        textarea:focus, input:focus { outline: none; border-color: #2563eb; }
        .btn-primary { width: 100%; padding: 1rem; border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; background: linear-gradient(135deg, #2563eb, #3b82f6); color: white; transition: all 0.3s; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4); }
        .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
        .loading { display: none; text-align: center; padding: 2rem; background: #f1f5f9; border-radius: 8px; margin-top: 1rem; }
        .spinner { border: 4px solid #f3f4f6; border-top: 4px solid #2563eb; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .result { display: none; margin-top: 2rem; padding-top: 2rem; border-top: 2px solid #e2e8f0; }
        .explanation-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 2rem; line-height: 1.8; white-space: pre-wrap; }
        .explanation-box h2 { color: #2563eb; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        .explanation-box h2:first-child { margin-top: 0; }
        footer { text-align: center; color: white; margin-top: 2rem; opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ 전기기사 공식 AI 설명 생성기</h1>
            <p>Claude AI로 공식을 쉽게 이해하세요</p>
        </header>
        <main>
            <div class="form-group">
                <label for="problem">문제 내용</label>
                <textarea id="problem" placeholder="예시: 평행판 커패시터의 극판 사이에 유전체를 채웠을 때 정전용량의 변화를 구하시오."></textarea>
            </div>
            <div class="form-group">
                <label for="formula">관련 공식</label>
                <input type="text" id="formula" placeholder="예시: C = ε₀εᵣA/d">
            </div>
            <button id="generateBtn" class="btn-primary">📖 설명 생성하기</button>
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>Claude가 설명 작성 중... (15-30초 소요)</p>
            </div>
            <div id="result" class="result">
                <h2>✨ 생성 결과</h2>
                <div id="explanation" class="explanation-box"></div>
            </div>
        </main>
        <footer>
            <p>Made with ❤️ by 전기공학 강사 | Powered by Claude API & Railway</p>
        </footer>
    </div>
    <script>
        const problemInput = document.getElementById('problem');
        const formulaInput = document.getElementById('formula');
        const generateBtn = document.getElementById('generateBtn');
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');
        const explanation = document.getElementById('explanation');

        generateBtn.addEventListener('click', async () => {
            const problem = problemInput.value.trim();
            const formula = formulaInput.value.trim();

            if (!problem || !formula) {
                alert('문제와 공식을 모두 입력해주세요.');
                return;
            }

            generateBtn.disabled = true;
            loading.style.display = 'block';
            result.style.display = 'none';

            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({problem, formula})
                });

                const data = await response.json();

                if (data.success) {
                    let html = data.explanation
                        .replace(/## (.*)/g, '<h2>$1</h2>')
                        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
                    explanation.innerHTML = html;
                    result.style.display = 'block';
                    result.scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert('오류: ' + data.error);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('서버 오류가 발생했습니다.');
            } finally {
                generateBtn.disabled = false;
                loading.style.display = 'none';
            }
        });

        formulaInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                generateBtn.click();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        problem_text = data.get('problem', '')
        formula = data.get('formula', '')
        
        if not problem_text or not formula:
            return jsonify({'success': False, 'error': '문제와 공식을 모두 입력해주세요.'}), 400
        
        content_hash = generate_hash(problem_text, formula)
        
        if content_hash in cache:
            return jsonify({
                'success': True,
                'cached': True,
                'explanation': cache[content_hash]['explanation']
            })
        
        explanation = generate_explanation(problem_text, formula)
        
        if not explanation:
            return jsonify({'success': False, 'error': 'API 키가 설정되지 않았거나 생성에 실패했습니다.'}), 500
        
        cache[content_hash] = {
            'explanation': explanation,
            'created_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'cached': False,
            'explanation': explanation
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({
        'success': True,
        'message': 'API is running',
        'api_key_set': bool(ANTHROPIC_API_KEY)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
