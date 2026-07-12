import re

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_04_escape_room.html")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Questions Data
qs = [
    {"qnum": 1, "title": "심해로 가는 좌표 (순서쌍과 좌표)", "story": "🌊 <strong>[목표 지점 확인]</strong><br><br>잠수정을 투하할 해수면 좌표를 계산해야 합니다. 조금이라도 좌표가 어긋나면 아틀란티스 유적으로 향하는 해류를 타지 못하고 암초에 부딪히게 됩니다.", "qtext": "<strong>Q1. [순서쌍 좌표 찍기]</strong><br>x좌표가 -5 이고, y좌표가 8 인 점의 <strong>좌표</strong>를 순서쌍 기호 괄호 ()를 사용하여 나타내시오.", "placeholder": "예: (3, 4)", "error": "투하 좌표가 어긋났습니다! 암초에 부딪힐 위험이 있습니다!", "ans_check": "ans === '-5,8'"},
    {"qnum": 2, "title": "심해로 가는 좌표", "story": "🌊 <strong>[투하 지점 갱신]</strong><br><br>좋습니다, 첫 번째 투하 지점을 통과했습니다. 다음 기착지인 해저 화산 입구를 통과하려면 x축 위의 점을 입력해야 합니다.", "qtext": "<strong>Q2. [x축, y축 위의 점]</strong><br>x축 위에 있고 x좌표가 7인 점의 좌표를 나타내시오.", "placeholder": "예: (2, 0)", "error": "좌표 입력 오류! 수압 경고!", "ans_check": "ans === '7,0'"},
    {"qnum": 3, "title": "심해로 가는 좌표", "story": "🌊 <strong>[기준점 확인]</strong><br><br>심해 내비게이션의 영점 조준이 필요합니다.", "qtext": "<strong>Q3. [원점의 좌표]</strong><br>두 좌표축이 만나는 원점 O의 좌표를 나타내시오.", "placeholder": "예: (x, y)", "error": "영점 조준 실패!", "ans_check": "ans === '0,0'"},
    {"qnum": 4, "title": "심해로 가는 좌표", "story": "🌊 <strong>[추가 기준점]</strong><br><br>y축 방향의 해저 동굴 입구 좌표를 입력하세요.", "qtext": "<strong>Q4. [좌표 평면 위의 점]</strong><br>y축 위에 있고 y좌표가 -3인 점의 좌표를 나타내시오.", "placeholder": "예: (0, -5)", "error": "동굴 충돌 위험!", "ans_check": "ans === '0,-3'"},
    {"qnum": 5, "title": "심해로 가는 좌표", "story": "🌊 <strong>[소용돌이 결계]</strong><br><br>레이더에 4개의 기둥 좌표가 찍혔습니다. 이 기둥들이 만드는 결계의 넓이를 구하세요.", "qtext": "<strong>Q5. [도형의 넓이]</strong><br>좌표평면 위에 네 기둥 A(3, 4), B(-3, 4), C(-3, -4), D(3, -4)를 이은 직사각형의 넓이를 구하시오.", "placeholder": "숫자만 입력", "error": "결계 돌파 실패!", "ans_check": "ans === '48'"},
    {"qnum": 6, "title": "아틀란티스의 사분면 결계", "story": "🧭 <strong>[사분면 분석]</strong><br><br>해저 유적 내부로 진입했습니다. 이곳은 4개의 구역(사분면)으로 나뉘어 있습니다.", "qtext": "<strong>Q6. [사분면의 부호 1]</strong><br>점 (2, -5)는 제 몇 사분면 위의 점인가?", "placeholder": "숫자만 입력 (예: 1)", "error": "잘못된 구역입니다!", "ans_check": "ans === '4'"},
    {"qnum": 7, "title": "아틀란티스의 사분면 결계", "story": "🧭 <strong>[추가 결계]</strong><br><br>두 번째 사분면 문을 엽니다.", "qtext": "<strong>Q7. [사분면의 부호 2]</strong><br>점 (-4, -7)은 제 몇 사분면 위의 점인가?", "placeholder": "숫자만 입력", "error": "잘못된 구역입니다!", "ans_check": "ans === '3'"},
    {"qnum": 8, "title": "아틀란티스의 사분면 결계", "story": "🧭 <strong>[고급 사분면]</strong><br><br>조건에 맞는 사분면을 찾아야 합니다.", "qtext": "<strong>Q8. [사분면의 이해]</strong><br>점 P(a, b)에 대하여 a × b < 0 이고 a - b > 0 일 때, 점 P는 제 몇 사분면 위에 있는지 구하시오.", "placeholder": "숫자만 입력", "error": "잘못된 구역입니다!", "ans_check": "ans === '4'"},
    {"qnum": 9, "title": "아틀란티스의 사분면 결계", "story": "🧭 <strong>[사분면 분석]</strong><br><br>결계의 성질을 이용해 새로운 좌표의 사분면을 예측해야 합니다.", "qtext": "<strong>Q9. [사분면의 응용 1]</strong><br>점 P(a, b)가 제2사분면 위의 점일 때, 점 Q(a, -b)는 제 몇 사분면 위의 점인가?", "placeholder": "숫자만 입력", "error": "잘못된 구역입니다!", "ans_check": "ans === '3'"},
    {"qnum": 10, "title": "아틀란티스의 사분면 결계", "story": "🧭 <strong>[결계 돌파]</strong><br><br>마지막 사분면 문을 열기 위해 부호를 반전시킨 좌표의 사분면을 알아내야 합니다.", "qtext": "<strong>Q10. [사분면의 응용 2]</strong><br>점 P(a, b)가 제3사분면 위의 점일 때, 점 Q(-a, b)는 제 몇 사분면 위의 점인가?", "placeholder": "숫자만 입력", "error": "잘못된 구역입니다!", "ans_check": "ans === '4'"},
    {"qnum": 11, "title": "해저 수압의 변화", "story": "🌊 <strong>[수압 경고]</strong><br><br>수압 그래프를 분석합니다.", "qtext": "<strong>Q11. [그래프 해석 1]</strong><br>x분 동안 이동한 거리 y m를 나타낸 그래프가 수평을 유지한 구간은 잠수정이 무엇을 의미하는가?", "placeholder": "예: 상승, 하강, 정지", "error": "그래프 해석 오류!", "ans_check": "ans === '정지'"},
    {"qnum": 12, "title": "해저 수압의 변화", "story": "🌊 <strong>[깊이 예측]</strong><br><br>일정한 속력으로 내려가는 잠수정의 깊이를 구합니다.", "qtext": "<strong>Q12. [그래프 해석 2]</strong><br>잠수정이 수심 100m까지 10분 동안 일정한 속력으로 내려갔다. 5분일 때 수심은 몇 m인가?", "placeholder": "숫자만 입력", "error": "깊이 예측 실패!", "ans_check": "ans === '50'"},
    {"qnum": 13, "title": "해저 수압의 변화", "story": "🌊 <strong>[그래프 방향]</strong><br><br>직선의 방향성을 파악합니다.", "qtext": "<strong>Q13. [그래프 해석 3]</strong><br>그래프가 원점을 지나는 우상향 직선일 때, x가 증가하면 y는 어떻게 되는가?", "placeholder": "예: 증가, 감소", "error": "해석 오류!", "ans_check": "ans === '증가'"},
    {"qnum": 14, "title": "해저 수압의 변화", "story": "🌊 <strong>[변화량 분석]</strong><br><br>정지 상태에서의 변화량을 확인합니다.", "qtext": "<strong>Q14. [그래프 해석 4]</strong><br>수심 100m에서 5분간 머물렀다. 이 5분 동안 깊이 y값의 변화량은 얼마인가?", "placeholder": "숫자만 입력", "error": "해석 오류!", "ans_check": "ans === '0'"},
    {"qnum": 15, "title": "해저 수압의 변화", "story": "🌊 <strong>[산소 잔량]</strong><br><br>남은 산소의 양을 그래프로 나타낼 때의 개형을 맞춥니다.", "qtext": "<strong>Q15. [변수 관계 이해]</strong><br>시간 x가 지남에 따라 남은 산소량 y를 그래프로 그리면, 우하향하는 모양인가 우상향하는 모양인가?", "placeholder": "예: 우하향, 우상향", "error": "산소 예측 실패!", "ans_check": "ans === '우하향'"},
    {"qnum": 16, "title": "황금 문 톱니바퀴", "story": "⚙️ <strong>[정비례 회전]</strong><br><br>황금 문을 여는 톱니바퀴의 회전수 관계를 파악합니다.", "qtext": "<strong>Q16. [정비례 관계]</strong><br>y가 x에 정비례하고, x=3일 때 y=15이다. x=5일 때 y의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "톱니바퀴가 멈췄습니다!", "ans_check": "ans === '25'"},
    {"qnum": 17, "title": "황금 문 톱니바퀴", "story": "⚙️ <strong>[비례 상수]</strong><br><br>함수식을 완성해야 다이얼이 돌아갑니다.", "qtext": "<strong>Q17. [정비례 함수식]</strong><br>y = ax의 그래프가 점 (2, -8)을 지날 때, 상수 a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "다이얼 번호 오류!", "ans_check": "ans === '-4'"},
    {"qnum": 18, "title": "황금 문 톱니바퀴", "story": "💎 <strong>[보물 적재 경보]</strong><br><br>황금을 챙겨가려면 부력 장치와 무게의 반비례 관계를 알아야 합니다.", "qtext": "<strong>Q18. [반비례 관계 1]</strong><br>부력 장치 x개와 1개당 감당할 무게 y kg은 반비례한다. 4개를 달면 60kg을 감당할 때, 6개로 늘리면 몇 kg을 감당해야 하는가?", "placeholder": "숫자만 입력", "error": "부력 균형 붕괴!", "ans_check": "ans === '40'"},
    {"qnum": 19, "title": "황금 문 톱니바퀴", "story": "💎 <strong>[반비례 상수]</strong><br><br>반비례 관계식을 알아냅니다.", "qtext": "<strong>Q19. [반비례 관계 2]</strong><br>y가 x에 반비례하고 x=2일 때 y=10이다. y = a/x에서 a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "식 계산 오류!", "ans_check": "ans === '20'"},
    {"qnum": 20, "title": "황금 문 톱니바퀴", "story": "🔴 <strong>[최종 탈출 레이저]</strong><br><br>마지막 탈출구를 엽니다!", "qtext": "<strong>Q20. [최종 암호 해독]</strong><br>반비례 그래프 y = 12/x 가 점 (-3, k)를 지난다. 최종 암호 k의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "레이저 방어막에 막혔습니다!", "ans_check": "ans === '-4'"}
]

# Generate panels

import re
def generate_hint(qnum, qtext, ans_check):
    if qnum == 1:
        return "순서쌍은 (x좌표, y좌표) 형태로 나타내며, 괄호와 쉼표를 정확히 표시합니다. 주어진 문제에서 x좌표와 y좌표가 무엇인지 찾아 차례대로 적어보세요."
    elif qnum == 2:
        return "x축 위에 있는 점들은 y축 방향으로 움직이지 않았으므로 y좌표가 항상 0입니다. 즉, (x좌표, 0)의 형태가 됩니다."
    elif qnum == 3:
        return "원점은 x축과 y축이 교차하는 시작점입니다. x좌표와 y좌표가 모두 0이 되는 지점을 순서쌍 형태로 나타내보세요."
    elif qnum == 4:
        return "y축 위에 있는 점들은 x축 방향으로 움직이지 않았으므로 x좌표가 항상 0입니다. 즉, (0, y좌표)의 형태가 됩니다."
    elif qnum == 5:
        return "직사각형의 가로 길이는 두 x좌표 사이의 거리이고, 세로 길이는 두 y좌표 사이의 거리입니다. 가로와 세로의 길이를 각각 구해 서로 곱해보세요."
    elif qnum == 6:
        return "x좌표가 양수(+)이고, y좌표가 음수(-)인 점이 어느 위치에 있는지 생각해 보세요. 좌표평면의 네 영역 중 우하단에 해당하는 영역을 찾으면 됩니다."
    elif qnum == 7:
        return "x좌표가 음수(-), y좌표가 음수(-)인 점이 어느 위치에 있는지 생각해 보세요. 좌표평면의 네 영역 중 좌하단에 해당하는 영역을 찾으면 됩니다."
    elif qnum == 8:
        return "곱이 음수(a × b < 0)라는 것은 두 수의 부호가 서로 다름을 뜻합니다. 뺀 값(a - b > 0)이 양수라는 것은 어느 쪽이 더 크다는 뜻일까요? 두 조건으로 a와 b의 부호를 판별해 보세요."
    elif qnum == 9:
        return "점 P가 제2사분면 위의 점일 때 a와 b의 부호를 먼저 정해봅니다. 그 후 -b의 부호가 어떻게 바뀌는지 알아내어 점 Q의 (x좌표, y좌표) 부호를 분석해 보세요."
    elif qnum == 10:
        return "점 P가 제3사분면 위의 점일 때 a와 b의 부호를 먼저 정해봅니다. 그 후 -a의 부호가 어떻게 바뀌는지 알아내어 점 Q의 (x좌표, y좌표) 부호를 분석해 보세요."
    elif qnum == 11:
        return "시간(x)은 계속 흘러가는데 이동한 거리(y)를 나타내는 그래프의 높이가 변하지 않고 평평합니다. 이는 잠수정이 어떤 상태임을 뜻할까요?"
    elif qnum == 12:
        return "일정한 속력으로 내려가므로 시간과 깊이는 정비례 관계입니다. 10분 동안 100m를 내려갔을 때, 절반의 시간인 5분 동안에는 몇 m를 내려갔을지 비례식을 세워 보세요."
    elif qnum == 13:
        return "우상향하는 직선은 오른쪽 위를 향합니다. 따라서 그래프 상에서 오른쪽(x가 커지는 방향)으로 이동할 때, 그래프의 세로 높이(y값)는 어떻게 변하는지 관찰해 보세요."
    elif qnum == 14:
        return "수심 100m 지점에 5분 동안 계속 가만히 멈춰 있었다면, 멈춰 있는 동안 깊이(y값)가 변한 양은 얼마일지 생각해 보세요."
    elif qnum == 15:
        return "시간(x)이 흐를수록 탱크 안에 남은 산소량(y)은 늘어날까요, 아니면 줄어들까요? 양의 변화에 따른 그래프의 방향(우상향 또는 우하향)을 결정해 보세요."
    elif qnum == 16:
        return "y가 x에 정비례하므로 식 y = ax를 세울 수 있습니다. 먼저 주어진 x = 3, y = 15를 대입해 비례상수 a의 값을 구한 후, 완성된 식에 x = 5를 대입해 보세요."
    elif qnum == 17:
        return "점 (2, -8)을 지난다는 것은 x = 2일 때 y = -8이 성립한다는 뜻입니다. 이 값을 y = ax 식에 대입하여 일차방정식을 풀어보세요."
    elif qnum == 18:
        return "두 변수 x, y가 반비례 관계일 때는 두 변수의 곱(x × y)이 항상 비례상수 a로 일정합니다. 먼저 4개일 때 60kg인 것을 이용해 곱을 구하고, 6개일 때의 무게를 계산해 보세요."
    elif qnum == 19:
        return "y가 x에 반비례하므로 y = a/x 식에 대입할 수 있습니다. 주어진 x = 2, y = 10을 대입하여 분수 식을 참으로 만드는 상수 a의 값을 구해 보세요."
    elif qnum == 20:
        return "점 (-3, k)가 반비례 그래프 위에 있으므로 x = -3, y = k를 식 y = 12/x에 대입하면 등식이 성립합니다. k값을 계산해 보세요."
    return "단위를 제외하고 입력해 보세요."

for q in qs:
    q['hint'] = generate_hint(q['qnum'], q['qtext'], q.get('ans_check', ''))

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
    
    # 💡 힌트 버튼을 질문 제목 <strong>Q{qnum}. [제목]</strong> 바로 옆에 삽입
    hint_btn_html = f'<button class="btn-hint" onclick="alert(\'💡 힌트: {q["hint"]}\')">💡 힌트</button>'
    qtext_hinted = qtext.replace('</strong>', f'</strong> {hint_btn_html}', 1)
    
    panel = f'''
        <!-- Q{qnum} -->
        <div id="panel_q{qnum}" class="glass-panel">
            <h2>제 {qnum}구역: {title} <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="assets/m1_04_coordinates/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">{story}</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="question-box">
                <div class="question-content">
                    {qtext_hinted}
                    <div class="input-group">
                        <input type="text" id="ans{qnum}" placeholder="{placeholder}">
                    </div>
                </div>
            </div>
            <div class="error-msg" id="error{qnum}">{error}</div>
            <div class="btn-group">
                <button class="btn" onclick="checkQ{qnum}()">{'잠항 시작' if qnum==1 and "update_app_04.py"=="update_app_04.py" else '미궁 진입' if qnum==1 and "update_app_04.py"=="update_app_06.py" else '시스템 복구 시작' if qnum==1 else '다음으로' if qnum < 20 else '탈출하기'}</button>
            </div>
        </div>
'''
    panels_html += panel

# Outro panel
outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>탈출 성공!</h1>
            <h2>아틀란티스의 보물</h2>
            <img src="assets/m1_04_coordinates/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">"패널에 숫자 '-4'를 입력하는 순간! 지잉- 하는 소리와 함께 해저 도시의 거대한 황금 문이 갈라집니다. 
                남은 산소는 단 2분. 여러분은 황금 문을 연 성취감을 안고, 잠수정의 부력 장치를 가동하여 보물상자와 함께 해수면을 향해 솟구쳐 오릅니다. 
                좌표평면과 비례 그래프의 지혜로 전설을 현실로 만들었습니다. 미션 대성공!"</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
panels_html += outro_html

# Generate JS checks
js_checks = ""
for q in qs:
    qnum = q['qnum']
    ans_check = q.get('ans_check', 'false')
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    victory_call = 'try { playVictory(); } catch(e) {}' if qnum == 20 else 'try { playSuccess(); } catch(e) {}'
    
    if qnum <= 5:
        reset_qnum = 1
        reset_prog = 0
        zone_name = "1구역"
    elif qnum <= 10:
        reset_qnum = 6
        reset_prog = 25
        zone_name = "2구역"
    elif qnum <= 15:
        reset_qnum = 11
        reset_prog = 50
        zone_name = "3구역"
    else:
        reset_qnum = 16
        reset_prog = 75
        zone_name = "4구역"

    gas_end_call = ""
    if qnum == 20:
        gas_end_call = '''
                // GAS 기록 종료 호출
                try {
                    if (window.userRecordRow && typeof google !== 'undefined' && google.script && google.script.run) {
                        google.script.run.recordEnd(window.userRecordRow, 'm1_04');
                    }
                } catch(e) {
                    console.warn("구글 시트 종료 기록 실패(로컬 테스트 모드):", e);
                }'''

    js = f'''
        // Q{qnum}
        function checkQ{qnum}() {{
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace('(','').replace(')','');
            if ({ans_check}) {{
                wrongCount = 0;
                {victory_call} {gas_end_call}
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
            }} else {{
                wrongCount++;
                if (wrongCount >= 3) {{
                    alert("🚨 3회 오답 패널티! {zone_name} 처음으로 이동됩니다.");
                    wrongCount = 0;
                    document.getElementById('ans{reset_qnum}').value = '';
                    nextStage('panel_q{qnum}', 'panel_q{reset_qnum}', {reset_prog});
                }} else {{
                    showError('panel_q{qnum}', 'error{qnum}');
                }}
            }}
        }}
'''
    js_checks += js


import re
new_content = re.sub(r'<!-- Q1.*?(?=<script>)', lambda m: '<!-- Q1 -->\n' + panels_html + '\n    ', content, flags=re.DOTALL)

new_content = re.sub(r'// Q1[\s\S]*?(?=window\.onload = \(\) => \{)', lambda m: '// Q1\n' + js_checks + '\n        ', new_content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated successfully.")
