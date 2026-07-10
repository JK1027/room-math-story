import re

html_file = 'app_m1_04_escape_room.html'

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
    {"qnum": 9, "title": "아틀란티스의 사분면 결계", "story": "🧭 <strong>[대칭 이동]</strong><br><br>함정에 빠지지 않으려면 대칭점의 좌표를 알아야 합니다.", "qtext": "<strong>Q9. [축에 대칭인 점]</strong><br>점 (3, 2)와 x축에 대하여 대칭인 점의 y좌표를 구하시오.", "placeholder": "숫자만 입력", "error": "함정에 걸렸습니다!", "ans_check": "ans === '-2'"},
    {"qnum": 10, "title": "아틀란티스의 사분면 결계", "story": "🧭 <strong>[최종 대칭]</strong><br><br>원점 대칭 거울방의 문을 엽니다.", "qtext": "<strong>Q10. [원점에 대칭인 점]</strong><br>점 (-1, 4)와 원점에 대하여 대칭인 점의 x좌표를 구하시오.", "placeholder": "숫자만 입력", "error": "거울방에 갇혔습니다!", "ans_check": "ans === '1'"},
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
            <h2>제 {qnum}구역: {title}</h2>
            <img src="assets/m1_04_coordinates/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">{story}</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
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
    ans_check = q['ans_check']
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    victory_call = 'playVictory();' if qnum == 20 else 'playSuccess();'
    
    js = f'''
        // Q{qnum}
        function checkQ{qnum}() {{
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace('(','').replace(')','');
            if ({ans_check}) {{
                {victory_call} 
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
            }} else {{
                showError('panel_q{qnum}', 'error{qnum}');
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
