import re

import os; html_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'apps/app_m1_07_escape_room.html')

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 스타일 확인 및 주입
css = """
        .panel-image {
            width: 100%;
            max-height: 250px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
"""
if '.panel-image {' not in content:
    content = content.replace('</style>', css + '</style>')

# intro 패널을 피라미드 테마로 교체
intro_pattern = r'<div id="intro" class="glass-panel active">[\s\S]*?</div>\s*</div>\s*<!-- Q1 -->'
intro_replacement = '''<div id="intro" class="glass-panel active">
            <h1>피라미드의 비밀</h1>
            <img src="assets/m1_07_solid_geometry/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                여러분은 이집트 사막 한가운데 숨겨져 있던 미지의 거대 피라미드를 탐사 중입니다. 왕의 무덤에 들어선 순간, 바닥이 꺼지며 깊은 지하 미궁으로 떨어졌습니다!<br><br>
                이 미궁은 입체도형의 마법으로 보호받고 있습니다. 다면체와 회전체의 성질을 이용해 함정을 피하고, 각종 도형의 겉넓이와 부피를 계산하여 20개의 암호를 풀어야만 지상으로 올라갈 수 있습니다.<br><br>
                산소는 딱 40분 남았습니다. 수학적 지혜를 발휘하여 피라미드를 탈출하세요!
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 0)">시스템 복구 시작</button>
            </div>
        </div>
        <!-- Q1 -->'''

content = re.sub(intro_pattern, intro_replacement, content)

qs = [
    {"qnum": 1, "title": "다면체의 방", "story": "🚨 <strong>[석상의 저주]</strong><br><br>방의 벽면이 조여옵니다! 다면체의 모서리와 꼭짓점 수를 정확히 세어야 벽이 멈춥니다!", "qtext": "<strong>Q1. [다면체의 이해]</strong><br>옆면이 모두 직사각형인 다면체를 무엇이라 부르는가? (힌트: 기둥)", "placeholder": "예: 각뿔", "error": "도형 이름 오류!", "ans_check": "ans === '각기둥'"},
    {"qnum": 2, "title": "다면체의 방", "story": "🚨 <strong>[꼭짓점 카운트]</strong><br><br>기둥의 꼭짓점을 세어야 합니다.", "qtext": "<strong>Q2. [꼭짓점의 개수]</strong><br>밑면이 오각형인 오각기둥의 꼭짓점의 개수를 구하시오.", "placeholder": "숫자만 입력", "error": "개수 오류!", "ans_check": "ans === '10'"},
    {"qnum": 3, "title": "다면체의 방", "story": "🚨 <strong>[모서리 확인]</strong><br><br>이번에는 뿔의 모서리입니다.", "qtext": "<strong>Q3. [모서리의 개수]</strong><br>밑면이 육각형인 육각뿔의 모서리의 개수를 구하시오.", "placeholder": "숫자만 입력", "error": "개수 오류!", "ans_check": "ans === '12'"},
    {"qnum": 4, "title": "다면체의 방", "story": "🚨 <strong>[뿔대의 면]</strong><br><br>뿔대의 면의 개수를 알아야 함정이 멈춥니다.", "qtext": "<strong>Q4. [면의 개수]</strong><br>사각뿔대의 면의 개수를 구하시오.", "placeholder": "숫자만 입력", "error": "개수 오류!", "ans_check": "ans === '6'"},
    {"qnum": 5, "title": "다면체의 방", "story": "🚨 <strong>[정다면체의 마법]</strong><br><br>벽이 거의 다가왔습니다! 정다면체의 이름을 맞추세요.", "qtext": "<strong>Q5. [정다면체]</strong><br>각 면이 모두 합동인 정삼각형이고 한 꼭짓점에 모이는 면의 개수가 3개인 정다면체의 이름을 구하시오.", "placeholder": "예: 정육면체", "error": "정다면체 이름 오류!", "ans_check": "ans === '정사면체'"},
    {"qnum": 6, "title": "파라오의 도자기", "story": "🏺 <strong>[도자기 복원]</strong><br><br>파쇄된 파라오의 항아리를 복원하려면 회전체의 단면을 알아야 합니다!", "qtext": "<strong>Q6. [회전체의 이해]</strong><br>평면도형을 한 직선을 축으로 하여 1회전 시킬 때 생기는 입체도형을 무엇이라 부르는가?", "placeholder": "예: 다면체", "error": "도형 종류 오류!", "ans_check": "ans === '회전체'"},
    {"qnum": 7, "title": "파라오의 도자기", "story": "🏺 <strong>[원기둥의 단면]</strong><br><br>원기둥 모양 도자기의 조각을 맞춥니다.", "qtext": "<strong>Q7. [회전축과 단면 1]</strong><br>원기둥을 회전축을 포함하는 평면으로 자를 때 생기는 단면의 모양은 무엇인가?", "placeholder": "예: 사각형", "error": "단면 모양 오류!", "ans_check": "ans === '직사각형'"},
    {"qnum": 8, "title": "파라오의 도자기", "story": "🏺 <strong>[원뿔의 단면]</strong><br><br>원뿔 모양 뚜껑의 단면입니다.", "qtext": "<strong>Q8. [회전축과 단면 2]</strong><br>원뿔을 회전축에 수직인 평면으로 자를 때 생기는 단면의 모양은 무엇인가?", "placeholder": "예: 타원", "error": "단면 모양 오류!", "ans_check": "ans === '원'"},
    {"qnum": 9, "title": "파라오의 도자기", "story": "🏺 <strong>[회전체 생성]</strong><br><br>직각삼각형 모양의 도구를 회전시켜야 합니다.", "qtext": "<strong>Q9. [회전체의 종류]</strong><br>직각삼각형을 직각을 낀 한 변을 축으로 하여 1회전 시키면 생기는 도형은 무엇인가?", "placeholder": "예: 원기둥", "error": "도형 이름 오류!", "ans_check": "ans === '원뿔'"},
    {"qnum": 10, "title": "파라오의 도자기", "story": "🏺 <strong>[구의 단면]</strong><br><br>가장 완벽한 도형, 구의 성질입니다.", "qtext": "<strong>Q10. [구의 성질]</strong><br>구를 어떤 평면으로 자르더라도 그 단면은 항상 어떤 모양인가?", "placeholder": "예: 타원", "error": "단면 오류!", "ans_check": "ans === '원'"},
    {"qnum": 11, "title": "황금 상자의 겉넓이", "story": "☀️ <strong>[황금 도금]</strong><br><br>파라오의 상자를 황금으로 도금해야 합니다. 도금할 겉넓이를 정확히 계산하세요!", "qtext": "<strong>Q11. [각기둥의 겉넓이]</strong><br>밑면이 가로 3cm, 세로 4cm인 직사각형이고, 높이가 5cm인 직육면체의 겉넓이를 구하시오.", "placeholder": "숫자만 입력", "error": "도금 면적 오류!", "ans_check": "ans === '94'"},
    {"qnum": 12, "title": "황금 상자의 겉넓이", "story": "☀️ <strong>[원통 도금]</strong><br><br>이번에는 원통 모양 상자입니다. (원주율은 π로 계산, 한글 '파이'로 입력)", "qtext": "<strong>Q12. [원기둥의 겉넓이]</strong><br>밑면의 반지름이 2cm이고 높이가 6cm인 원기둥의 겉넓이를 구하시오.", "placeholder": "예: 10파이", "error": "도금 면적 오류!", "ans_check": "ans === '32파이'"},
    {"qnum": 13, "title": "황금 상자의 겉넓이", "story": "☀️ <strong>[피라미드 도금]</strong><br><br>정사각뿔 모양 뚜껑을 도금해야 합니다.", "qtext": "<strong>Q13. [사각뿔의 겉넓이]</strong><br>밑면이 한 변의 길이가 4cm인 정사각형이고, 옆면의 삼각형의 높이가 5cm인 정사각뿔의 겉넓이를 구하시오.", "placeholder": "숫자만 입력", "error": "도금 면적 오류!", "ans_check": "ans === '56'"},
    {"qnum": 14, "title": "황금 상자의 겉넓이", "story": "☀️ <strong>[원뿔 도금]</strong><br><br>원뿔 모양 제단을 도금합니다.", "qtext": "<strong>Q14. [원뿔의 겉넓이]</strong><br>밑면의 반지름이 3cm이고, 모선의 길이가 5cm인 원뿔의 겉넓이를 구하시오.", "placeholder": "예: 10파이", "error": "도금 면적 오류!", "ans_check": "ans === '24파이'"},
    {"qnum": 15, "title": "황금 상자의 겉넓이", "story": "☀️ <strong>[황금 구슬]</strong><br><br>장식용 구슬을 완전히 도금해야 합니다.", "qtext": "<strong>Q15. [구의 겉넓이]</strong><br>반지름의 길이가 3cm인 구의 겉넓이를 구하시오.", "placeholder": "예: 10파이", "error": "도금 면적 오류!", "ans_check": "ans === '36파이'"},
    {"qnum": 16, "title": "생명의 물 채우기", "story": "🔑 <strong>[마지막 관문]</strong><br><br>탈출 장치를 가동하려면 여러 입체도형 모양의 수조에 생명의 물을 정확한 부피만큼 채워야 합니다!", "qtext": "<strong>Q16. [각기둥의 부피]</strong><br>밑면의 넓이가 20cm²이고 높이가 8cm인 각기둥의 부피를 구하시오.", "placeholder": "숫자만 입력", "error": "수압 조절 실패!", "ans_check": "ans === '160'"},
    {"qnum": 17, "title": "생명의 물 채우기", "story": "🔑 <strong>[원기둥 수조]</strong><br><br>가장 큰 원통 수조에 물을 채웁니다.", "qtext": "<strong>Q17. [원기둥의 부피]</strong><br>밑면의 반지름이 4cm이고 높이가 5cm인 원기둥의 부피를 구하시오.", "placeholder": "예: 10파이", "error": "물이 넘칩니다!", "ans_check": "ans === '80파이'"},
    {"qnum": 18, "title": "생명의 물 채우기", "story": "🔑 <strong>[원뿔 수조]</strong><br><br>원뿔 수조에 물을 조심스럽게 채웁니다.", "qtext": "<strong>Q18. [원뿔의 부피]</strong><br>밑면의 반지름이 3cm이고 높이가 4cm인 원뿔의 부피를 구하시오.", "placeholder": "예: 10파이", "error": "물이 넘칩니다!", "ans_check": "ans === '12파이'"},
    {"qnum": 19, "title": "생명의 물 채우기", "story": "🔑 <strong>[둥근 수조]</strong><br><br>구 모양 수조의 부피를 계산하세요.", "qtext": "<strong>Q19. [구의 부피]</strong><br>반지름의 길이가 3cm인 구의 부피를 구하시오.", "placeholder": "예: 10파이", "error": "물이 부족합니다!", "ans_check": "ans === '36파이'"},
    {"qnum": 20, "title": "생명의 물 채우기", "story": "🔑 <strong>[최종 비밀 코드]</strong><br><br>모든 수조에 물이 찼습니다! 마지막 비밀 코드를 입력하세요.", "qtext": "<strong>Q20. [부피의 비]</strong><br>밑면의 반지름과 높이가 모두 같은 원뿔, 구, 원기둥의 부피의 비를 구하시오.", "placeholder": "예: 1:2:3", "error": "코드가 틀렸습니다!", "ans_check": "ans === '1:2:3'"}
]

# Generate panels

import re
def generate_hint(qtext, ans_check):
    qtext_clean = qtext.lower()
    
    if '소인수분해' in qtext_clean: return "주어진 수를 가장 작은 소수부터 차례대로 나누어 소수들의 곱으로 나타내보세요. (거듭제곱 기호 ^ 사용)"
    elif '최대공약수' in qtext_clean: return "공통된 소인수 중 지수가 같거나 가장 작은 것을 선택하여 모두 곱합니다."
    elif '최소공배수' in qtext_clean: return "모든 소인수를 선택하고, 공통된 소인수는 지수가 같거나 가장 큰 것을 선택하여 곱합니다."
    elif '정수' in qtext_clean and '유리수' in qtext_clean: return "양의 부호(+)나 음의 부호(-)를 주의해서 계산하세요. (음수×음수=양수)"
    elif '절댓값' in qtext_clean: return "절댓값은 수직선에서 원점으로부터의 거리이므로 항상 0보다 크거나 같습니다."
    elif '일차방정식' in qtext_clean and '해' in qtext_clean: return "미지수 x를 포함한 항은 좌변으로, 상수는 우변으로 이항하여 x = (숫자) 형태로 만드세요."
    elif '일차함수' in qtext_clean and '기울기' in qtext_clean: return "일차함수 y = ax + b 에서 x의 계수 a가 기울기를 의미합니다."
    elif '일차함수' in qtext_clean and ('y절편' in qtext_clean or 'x절편' in qtext_clean): return "y절편은 x=0일 때의 y값(b), x절편은 y=0일 때의 x값(-b/a)입니다."
    elif '연립방정식' in qtext_clean: return "가감법(두 식을 적절히 곱해 더하거나 빼기)이나 대입법을 사용하여 한 미지수를 먼저 없애보세요."
    elif '부등식' in qtext_clean: return "부등식의 양변에 음수를 곱하거나 나누면 부등호의 방향이 반대로 바뀐다는 점을 잊지 마세요."
    elif '경우의 수' in qtext_clean: return "동시에(연달아) 일어나는 사건은 곱의 법칙(×), 따로 일어나는 사건은 합의 법칙(+)을 적용하세요."
    elif '확률' in qtext_clean: return "(특정 사건이 일어날 경우의 수) / (모든 경우의 수) 로 계산한 분수 형태를 구하세요."
    elif '부피' in qtext_clean and '구' in qtext_clean: return "구의 부피 공식은 4/3 × 파이 × r³ 입니다."
    elif '겉넓이' in qtext_clean and '구' in qtext_clean: return "구의 겉넓이 공식은 4 × 파이 × r² 입니다."
    elif '부피' in qtext_clean and '기둥' in qtext_clean: return "기둥의 부피는 (밑넓이 × 높이) 입니다."
    elif '부피' in qtext_clean and '뿔' in qtext_clean: return "뿔의 부피는 1/3 × (밑넓이 × 높이) 입니다."
    elif '겉넓이' in qtext_clean: return "겉넓이는 전개도를 그렸을 때 모든 면의 넓이의 합입니다."
    elif '다각형' in qtext_clean and '내각' in qtext_clean: return "n각형의 내각의 크기의 합은 180° × (n - 2) 입니다."
    elif '다각형' in qtext_clean and '대각선' in qtext_clean: return "n각형의 대각선의 총 개수는 n(n - 3) / 2 입니다."
    elif '외각' in qtext_clean: return "다각형의 모든 외각의 크기의 합은 항상 360° 입니다."
    elif '닮음비' in qtext_clean: return "닮음비가 m:n 이면, 넓이비는 m²:n², 부피비는 m³:n³ 입니다."
    elif '피타고라스' in qtext_clean or '직각삼각형' in qtext_clean: return "직각삼각형에서 빗변의 길이의 제곱은 나머지 두 변의 길이의 제곱의 합과 같습니다. (a² + b² = c²)"
    elif '소수' in qtext_clean and '합' in qtext_clean: return "1과 자기 자신만을 약수로 가지는 수를 소수라고 합니다. (예: 2, 3, 5, 7...)"
    elif '좌표' in qtext_clean: return "x축의 좌표를 먼저, y축의 좌표를 나중에 (x, y) 형태로 생각해보세요."

    if '파이' in ans_check or 'pi' in ans_check: return "계산된 원주율은 기호 대신 한글 '파이'라고 적어주세요. (예: 36파이)"
    if '(' in ans_check and ',' in ans_check: return "순서쌍은 괄호나 띄어쓰기 없이 숫자와 쉼표로만 입력하거나 (x,y) 형태로 정확히 입력해보세요."
    
    ans_list = []
    if '||' in ans_check:
        ans_list = [a.strip().strip("'\"") for a in ans_check.split('||')]
        valid_ans = [a for a in ans_list if 'ans ===' in a]
        if valid_ans:
            first_ans = valid_ans[0].replace('ans === ', '').strip("'\"")
            return f"단위가 있다면 제외해보고, 기호 유무를 확인하세요. (정답 길이: 약 {len(first_ans)}글자)"
    else:
        match = re.search(r"ans === '([^']+)'", ans_check)
        if match:
            ans = match.group(1)
            if ans.isdigit(): return f"계산 실수가 없는지 다시 확인해보세요. 정답은 {len(ans)}자리 숫자입니다."
            else: return f"정답은 기호나 문자를 포함해 총 {len(ans)}글자입니다."
            
    return "단위(cm, 개 등)를 생략하거나 기호가 정확히 일치하는지 확인해 보세요."

for q in qs:
    q['hint'] = generate_hint(q['qtext'], q.get('ans_check', ''))

panels_html = ""
for i, q in enumerate(qs):
    qnum = q['qnum']
    title = q['title']
    story = q['story']
    qtext = q['qtext']
    placeholder = q['placeholder']
    error = q['error']
    
    prev_stage = f"'panel_q{qnum-1}'" if qnum > 1 else "'intro'"
    prev_progress = (qnum-1)*5
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    
    panel = f'''
        <!-- Q{qnum} -->
        <div id="panel_q{qnum}" class="glass-panel">
            <h2>제 {qnum}구역: {title} <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="assets/m1_07_solid_geometry/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                {story}
            </div>
            <div class="question-box">
                <div class="question-content">
                    {qtext}
                    <div class="input-group">
                        <input type="text" id="ans{qnum}" placeholder="{placeholder}">
                    </div>
                </div>
            </div>
            <div class="error-msg" id="error{qnum}">{error}</div>
            <div class="btn-group">
                <button class="btn btn-secondary" onclick="prevStage('panel_q{qnum}', {prev_stage}, {prev_progress})">이전 단서</button>
                <button class="btn" onclick="checkQ{qnum}()">{'미궁 진입' if qnum==1 else '다음으로' if qnum < 20 else '탈출하기'}</button>
            </div>
        </div>
'''
    panels_html += panel

# Outro panel
outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>탈출 성공!</h1>
            <h2>피라미드의 비밀</h2>
            <img src="assets/m1_07_solid_geometry/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                여러분들이 마지막 암호 '1:2:3'을 입력하자, 굳게 닫혀 있던 피라미드의 천장이 열리며 쏟아지는 모래 사이로 한 줄기 눈부신 햇살이 들어옵니다! 
                마법의 모래시계가 멈추고, 여러분은 부피의 비율에 맞춰 차오른 생명의 물기둥을 타고 지상으로 무사히 떠오릅니다. 
                다면체와 회전체의 성질, 그리고 겉넓이와 부피의 비밀을 완벽하게 파헤친 여러분, 고대 이집트 미궁 탈출에 대성공했습니다!
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
panels_html += outro_html

# Generate JS checks
js_checks = ""
for q in qs:
    qnum = q['qnum']
    ans_check = q['ans_check']
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    victory_call = 'playVictory();' if qnum == 20 else 'playSuccess();'
    
    js = f'''
        // Q{qnum}
        function checkQ{qnum}() {{
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace(/\\s+/g, '');
            if ({ans_check}) {{
                {victory_call} 
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
            }} else {{
                showError('panel_q{qnum}', 'error{qnum}');
            }}
        }}
'''
    js_checks += js

# Replace in content
start_panel_idx = content.find('<!-- Q1 -->')
end_panel_idx = content.find('        <script>', start_panel_idx)

if start_panel_idx != -1 and end_panel_idx != -1:
    content = content[:start_panel_idx] + panels_html + content[end_panel_idx:]

start_js_idx = content.find('        // Q1\n')
if start_js_idx == -1:
    start_js_idx = content.find('        // Q1\r\n')
end_js_idx = content.find('        window.onload = () => {', start_js_idx)

if start_js_idx != -1 and end_js_idx != -1:
    content = content[:start_js_idx] + js_checks + content[end_js_idx:]

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("App 07 updated successfully with images.")
