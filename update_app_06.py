import re

html_file = 'app_m1_06_escape_room.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

qs = [
    {"qnum": 1, "title": "빛의 반사각 조율", "story": "🚨 <strong>[대원의 비명]</strong><br><br>앗 뜨거워! 천장에서 빛줄기가 내려오고 있습니다. 거울 기둥들을 교차시켜 빛을 분산시켜야 합니다!", "qtext": "<strong>Q1. [다각형의 대각선 1]</strong><br>한 꼭짓점에서 그을 수 있는 대각선의 개수가 5개인 다각형의 이름을 구하시오.", "placeholder": "예: 육각형", "error": "기둥 조작 오류!", "ans_check": "ans === '팔각형'"},
    {"qnum": 2, "title": "빛의 반사각 조율", "story": "🚨 <strong>[대각선 교차]</strong><br><br>전체 대각선의 수를 계산해야 합니다.", "qtext": "<strong>Q2. [다각형의 대각선 2]</strong><br>십각형 모양의 기둥 배치에서 모든 기둥끼리 서로 빛을 교차 연결하려고 한다. 총 대각선의 개수를 구하시오.", "placeholder": "숫자만 입력", "error": "계산 오류!", "ans_check": "ans === '35'"},
    {"qnum": 3, "title": "빛의 반사각 조율", "story": "🚨 <strong>[빛의 굴절]</strong><br><br>빛이 새어나가고 있어요! 삼각형 반사판의 외각을 계산하세요.", "qtext": "<strong>Q3. [삼각형의 외각 1]</strong><br>삼각형 반사판에서 두 내각이 각각 45도, 60도일 때, 나머지 한 내각의 외각의 크기를 구하시오.", "placeholder": "숫자만 입력", "error": "각도 오류!", "ans_check": "ans === '105'"},
    {"qnum": 4, "title": "빛의 반사각 조율", "story": "🚨 <strong>[외각의 비율]</strong><br><br>외각의 비례식을 풀어야 합니다.", "qtext": "<strong>Q4. [삼각형의 외각 2]</strong><br>삼각형의 세 외각의 비가 2:3:4일 때, 가장 큰 외각의 크기를 구하시오.", "placeholder": "숫자만 입력", "error": "비율 오류!", "ans_check": "ans === '160'"},
    {"qnum": 5, "title": "빛의 반사각 조율", "story": "🚨 <strong>[내각의 합]</strong><br><br>마지막 반사판의 구조를 파악하세요.", "qtext": "<strong>Q5. [다각형의 내각]</strong><br>내각의 크기의 합이 900도인 다각형의 꼭짓점의 개수를 구하시오.", "placeholder": "숫자만 입력", "error": "다각형 모양 오류!", "ans_check": "ans === '7'"},
    {"qnum": 6, "title": "신전 바닥의 암호판", "story": "🧩 <strong>[비밀통로 발견]</strong><br><br>바닥에 거대한 회전 다이얼이 보입니다. 다각형의 내각과 외각의 합을 알아내면 통로가 열릴 겁니다!", "qtext": "<strong>Q6. [다각형의 외각의 합]</strong><br>모든 다각형의 외각의 크기의 합은 항상 일정합니다. 그 크기는 몇 도인가?", "placeholder": "숫자만 입력", "error": "회전판이 멈췄습니다!", "ans_check": "ans === '360'"},
    {"qnum": 7, "title": "신전 바닥의 암호판", "story": "🧩 <strong>[정다각형의 외각]</strong><br><br>외각의 크기로 다각형의 모양을 유추하세요.", "qtext": "<strong>Q7. [정다각형의 외각]</strong><br>한 외각의 크기가 36도인 정다각형의 이름을 구하시오.", "placeholder": "예: 정오각형", "error": "다이얼 문양 오류!", "ans_check": "ans === '정십각형'"},
    {"qnum": 8, "title": "신전 바닥의 암호판", "story": "🧩 <strong>[정다각형의 내각 1]</strong><br><br>팔각형 다이얼의 내각을 맞추세요.", "qtext": "<strong>Q8. [정다각형의 내각 1]</strong><br>정팔각형의 한 내각의 크기를 구하시오.", "placeholder": "숫자만 입력", "error": "각도 입력 실패!", "ans_check": "ans === '135'"},
    {"qnum": 9, "title": "신전 바닥의 암호판", "story": "🧩 <strong>[정다각형의 내각 2]</strong><br><br>다이얼의 대각선 개수를 계산해야 문이 열립니다.", "qtext": "<strong>Q9. [정다각형의 내각 2]</strong><br>한 내각의 크기가 150도인 정다각형의 대각선의 총 개수를 구하시오.", "placeholder": "숫자만 입력", "error": "계산 오류!", "ans_check": "ans === '54'"},
    {"qnum": 10, "title": "신전 바닥의 암호판", "story": "🧩 <strong>[내각과 외각의 비]</strong><br><br>마지막 암호판의 정체를 파악하세요.", "qtext": "<strong>Q10. [내각과 외각의 비]</strong><br>한 내각과 한 외각의 크기의 비가 4:1인 정다각형의 이름을 구하시오.", "placeholder": "예: 정육각형", "error": "암호판 고정 실패!", "ans_check": "ans === '정십각형'"},
    {"qnum": 11, "title": "태양 신의 석판 봉인", "story": "☀️ <strong>[거대 톱니바퀴]</strong><br><br>문이 조금 열렸습니다! 완전히 열려면 테두리의 석판을 정비례 원리를 이용해 돌려야 합니다!", "qtext": "<strong>Q11. [호의 길이와 중심각 1]</strong><br>한 원에서 부채꼴의 호의 길이는 중심각의 크기에 어떻게 비례하는가?", "placeholder": "예: 정비례, 반비례", "error": "비례 원리 오류!", "ans_check": "ans === '정비례'"},
    {"qnum": 12, "title": "태양 신의 석판 봉인", "story": "☀️ <strong>[호의 길이 비례식]</strong><br><br>중심각을 늘려서 석판을 더 많이 돌려야 합니다.", "qtext": "<strong>Q12. [호의 길이와 중심각 2]</strong><br>중심각이 40도일 때 호의 길이가 6cm라면, 중심각이 160도일 때 호의 길이를 구하시오.", "placeholder": "숫자만 입력", "error": "호의 길이 조절 실패!", "ans_check": "ans === '24'"},
    {"qnum": 13, "title": "태양 신의 석판 봉인", "story": "☀️ <strong>[부채꼴의 넓이 비율]</strong><br><br>빛을 모을 넓이의 비율을 맞추세요.", "qtext": "<strong>Q13. [부채꼴의 넓이와 중심각]</strong><br>부채꼴의 넓이가 원의 넓이의 1/6일 때, 이 부채꼴의 중심각의 크기를 구하시오.", "placeholder": "숫자만 입력", "error": "각도 조절 실패!", "ans_check": "ans === '60'"},
    {"qnum": 14, "title": "태양 신의 석판 봉인", "story": "☀️ <strong>[현의 성질]</strong><br><br>두 개의 열쇠 구멍의 길이가 같은지 확인합니다.", "qtext": "<strong>Q14. [현의 길이]</strong><br>중심각의 크기가 같은 두 부채꼴의 현의 길이는 서로 같은가?", "placeholder": "예: 같다, 다르다", "error": "현의 길이 오류!", "ans_check": "ans === '같다'"},
    {"qnum": 15, "title": "태양 신의 석판 봉인", "story": "☀️ <strong>[현과 중심각의 비례]</strong><br><br>비례 관계를 정확히 이해해야 다음으로 넘어갈 수 있습니다.", "qtext": "<strong>Q15. [현과 중심각의 비례]</strong><br>현의 길이는 중심각의 크기에 정비례하는가?", "placeholder": "예: 그렇다, 아니다", "error": "비례 관계 오류!", "ans_check": "ans === '아니다'"},
    {"qnum": 16, "title": "최종 냉각 수조", "story": "🔑 <strong>[마지막 관문]</strong><br><br>드디어 수조 앞입니다! 수조의 덮개를 열려면 부채꼴 모양 청동 열쇠의 넓이와 둘레를 정확히 계산해야 합니다!", "qtext": "<strong>Q16. [원주 계산]</strong><br>반지름의 길이가 5cm인 원의 둘레의 길이를 구하시오. (원주율은 π, 입력시 '파이'로 기재)", "placeholder": "예: 5파이", "error": "둘레 계산 오류!", "ans_check": "ans === '10파이'"},
    {"qnum": 17, "title": "최종 냉각 수조", "story": "🔑 <strong>[청동 열쇠 호의 길이]</strong><br><br>청동 열쇠 테두리에 금실을 둘러야 합니다.", "qtext": "<strong>Q17. [호의 길이 계산]</strong><br>반지름의 길이가 9cm이고 중심각의 크기가 120도인 부채꼴의 호의 길이를 구하시오.", "placeholder": "예: 3파이", "error": "금실 길이 부족!", "ans_check": "ans === '6파이'"},
    {"qnum": 18, "title": "최종 냉각 수조", "story": "🔑 <strong>[부채꼴 홈의 넓이]</strong><br><br>화강암 판 위에 에너지를 모을 면적을 계산하세요.", "qtext": "<strong>Q18. [부채꼴의 넓이 계산]</strong><br>반지름의 길이가 6cm이고 중심각의 크기가 60도인 부채꼴 모양 홈의 넓이를 구하시오.", "placeholder": "예: 2파이", "error": "면적 계산 오류!", "ans_check": "ans === '6파이'"},
    {"qnum": 19, "title": "최종 냉각 수조", "story": "🔑 <strong>[비상 게이트 수치]</strong><br><br>중심각을 모르는 상태에서 넓이를 계산해야 합니다.", "qtext": "<strong>Q19. [중심각 없이 넓이 구하기]</strong><br>반지름의 길이가 10cm이고 호의 길이가 5π cm인 부채꼴 모양 석문의 넓이를 계산하시오.", "placeholder": "예: 10파이", "error": "게이트 수치 오류!", "ans_check": "ans === '25파이'"},
    {"qnum": 20, "title": "최종 냉각 수조", "story": "🔑 <strong>[최종 탈출]</strong><br><br>마지막 암호 다이얼입니다! 색칠된 넓이를 맞추세요.", "qtext": "<strong>Q20. [색칠한 부분의 넓이]</strong><br>반지름이 8cm인 반원에서 반지름이 4cm인 반원 두 개를 뺀 색칠된 부분의 넓이를 구하시오.", "placeholder": "예: 12파이", "error": "다이얼이 잠겼습니다!", "ans_check": "ans === '16파이'"}
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
            <img src="assets/m1_06_plane_geometry/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                {story}
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
                <button class="btn" onclick="checkQ{qnum}()">{'잠항 시작' if qnum==1 and "update_app_06.py"=="update_app_04.py" else '미궁 진입' if qnum==1 and "update_app_06.py"=="update_app_06.py" else '시스템 복구 시작' if qnum==1 else '다음으로' if qnum < 20 else '탈출하기'}</button>
            </div>
        </div>
'''
    panels_html += panel

# Outro panel
outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>탈출 성공!</h1>
            <h2>태양 신전의 거울 미궁</h2>
            <img src="assets/m1_06_plane_geometry/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                여러분들이 땀을 흘리며 석문에 정답을 입력하고 다이얼을 돌리는 순간! 
                천장에서 쏟아지던 뜨겁고 살인적인 빛줄기가 마지막 거울에 반사되어 지하에 있는 깊은 냉각 수조의 중심부로 정확히 꽂힙니다. 
                쉭-! 하는 굉음과 함께 하얀 수증기가 신전을 가득 채우더니, 이내 굳게 닫혀 있던 탈출용 거대 돌벽이 스르륵 내려앉습니다. 
                눈을 뜰 수 없이 밝은 사막의 태양과 시원한 모래바람이 밀려옵니다. 거울 미궁 탈출에 성공했습니다!
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


# We use regex to replace everything between the start of the first panel and <script> tag
import re
new_content = re.sub(r'<!-- Q1.*?<script>', lambda m: '<!-- Q1 -->\n' + panels_html + '\n        <script>', content, flags=re.DOTALL)

# And for JS:
new_content = re.sub(r'// Q1[\s\S]*?window\.onload = \(\) => \{', lambda m: '// Q1\n' + js_checks + '\n        window.onload = () => {', new_content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("App 06 updated successfully with regex.")
