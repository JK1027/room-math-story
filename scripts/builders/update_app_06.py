import re

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_06_escape_room.html")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

qs = [
    {"qnum": 1, "title": "빛의 반사각 조율", "story": "🚨 <strong>[대원의 비명]</strong><br><br>앗 뜨거워! 천장에서 빛줄기가 내려오고 있습니다. 거울 기둥들을 교차시켜 빛을 분산시켜야 합니다!", "qtext": "<strong>Q1. [다각형의 대각선 1]</strong><br>한 꼭짓점에서 그을 수 있는 대각선의 개수가 5개인 다각형의 이름을 구하시오.", "placeholder": "예: 육각형", "error": "기둥 조작 오류!", "ans_check": "ans === '팔각형'", "hint": "n각형의 한 꼭짓점에서 그을 수 있는 대각선의 개수 공식은 n-3 입니다."},
    {"qnum": 2, "title": "빛의 반사각 조율", "story": "🚨 <strong>[대각선 교차]</strong><br><br>전체 대각선의 수를 계산해야 합니다.", "qtext": "<strong>Q2. [다각형의 대각선 2]</strong><br>십각형 모양의 기둥 배치에서 모든 기둥끼리 서로 빛을 교차 연결하려고 한다. 총 대각선의 개수를 구하시오.", "placeholder": "숫자만 입력", "error": "계산 오류!", "ans_check": "ans === '35'", "hint": "n각형의 총 대각선 수 공식인 n(n-3)/2 에 10을 대입하여 계산합니다."},
    {"qnum": 3, "title": "빛의 반사각 조율", "story": "🚨 <strong>[빛의 굴절]</strong><br><br>빛이 새어나가고 있어요! 삼각형 반사판의 외각을 계산하세요.", "qtext": "<strong>Q3. [삼각형의 외각 1]</strong><br>삼각형 반사판에서 두 내각이 각각 45도, 60도일 때, 나머지 한 내각의 외각의 크기를 구하시오.", "placeholder": "숫자만 입력", "error": "각도 오류!", "ans_check": "ans === '105'", "hint": "삼각형의 한 외각의 크기는 그와 이웃하지 않는 두 내각의 크기의 합과 같습니다."},
    {"qnum": 4, "title": "빛의 반사각 조율", "story": "🚨 <strong>[외각의 비율]</strong><br><br>외각의 비례식을 풀어야 합니다.", "qtext": "<strong>Q4. [삼각형의 외각 2]</strong><br>삼각형의 세 외각의 비가 2:3:4일 때, 가장 큰 외각의 크기를 구하시오.", "placeholder": "숫자만 입력", "error": "비율 오류!", "ans_check": "ans === '160'", "hint": "다각형의 외각의 총합은 항상 360도입니다. 비례배분을 이용하여 가장 큰 비율(4)을 차지하는 외각을 구합니다."},
    {"qnum": 5, "title": "빛의 반사각 조율", "story": "🚨 <strong>[내각의 합]</strong><br><br>마지막 반사판의 구조를 파악하세요.", "qtext": "<strong>Q5. [다각형의 내각]</strong><br>내각의 크기의 합이 900도인 다각형의 꼭짓점의 개수를 구하시오.", "placeholder": "숫자만 입력", "error": "다각형 모양 오류!", "ans_check": "ans === '7'", "hint": "n각형의 내각의 총합 공식은 180 * (n-2) 입니다. 이 값이 900이 되는 n을 찾습니다."},
    {"qnum": 6, "title": "신전 바닥의 암호판", "story": "🧩 <strong>[비밀통로 발견]</strong><br><br>바닥에 거대한 회전 다이얼이 보입니다. 다각형의 내각과 외각의 합을 알아내면 통로가 열릴 겁니다!", "qtext": "<strong>Q6. [다각형의 외각의 합]</strong><br>모든 다각형의 외각의 크기의 합은 항상 일정합니다. 그 크기는 몇 도인가?", "placeholder": "숫자만 입력", "error": "회전판이 멈췄습니다!", "ans_check": "ans === '360'", "hint": "다각형이 몇 각형이든 상관없이 모든 외각의 크기의 총합은 항상 360도입니다."},
    {"qnum": 7, "title": "신전 바닥의 암호판", "story": "🧩 <strong>[정다각형의 외각]</strong><br><br>외각의 크기로 다각형의 모양을 유추하세요.", "qtext": "<strong>Q7. [정다각형의 외각]</strong><br>한 외각의 크기가 36도인 정다각형의 이름을 구하시오.", "placeholder": "예: 정오각형", "error": "다이얼 문양 오류!", "ans_check": "ans === '정십각형'", "hint": "정n각형의 한 외각 크기는 360 / n 입니다. 이 값이 36이 되는 n을 구해 정다각형 이름을 적습니다."},
    {"qnum": 8, "title": "신전 바닥의 암호판", "story": "🧩 <strong>[정다각형의 내각 1]</strong><br><br>팔각형 다이얼의 내각을 맞추세요.", "qtext": "<strong>Q8. [정다각형의 내각 1]</strong><br>정팔각형의 한 내각의 크기를 구하시오.", "placeholder": "숫자만 입력", "error": "각도 입력 실패!", "ans_check": "ans === '135'", "hint": "정팔각형의 내각 총합인 180 * (8-2) = 1080도를 꼭짓점 개수인 8로 나누어 한 내각을 구합니다."},
    {"qnum": 9, "title": "신전 바닥의 암호판", "story": "🧩 <strong>[정다각형의 내각 2]</strong><br><br>다이얼의 대각선 개수를 계산해야 문이 열립니다.", "qtext": "<strong>Q9. [정다각형의 내각 2]</strong><br>한 내각의 크기가 150도인 정다각형의 대각선의 총 개수를 구하시오.", "placeholder": "숫자만 입력", "error": "계산 오류!", "ans_check": "ans === '54'", "hint": "한 내각이 150도이면 한 외각은 30도입니다. 외각의 합이 360도이므로 정십이각형임을 구한 뒤 총 대각선 공식을 적용합니다."},
    {"qnum": 10, "title": "신전 바닥의 암호판", "story": "🧩 <strong>[내각과 외각의 비]</strong><br><br>마지막 암호판의 정체를 파악하세요.", "qtext": "<strong>Q10. [내각과 외각의 비]</strong><br>한 내각과 한 외각의 크기의 비가 4:1인 정다각형의 이름을 구하시오.", "placeholder": "예: 정육각형", "error": "암호판 고정 실패!", "ans_check": "ans === '정십각형'", "hint": "한 내각과 한 외각의 합은 180도입니다. 이를 4:1로 비례배분하여 한 외각을 구하고 다각형 이름을 유추합니다."},
    {"qnum": 11, "title": "태양 신의 석판 봉인", "story": "☀️ <strong>[거대 톱니바퀴]</strong><br><br>문이 조금 열렸습니다! 완전히 열려면 테두리의 석판을 정비례 원리를 이용해 돌려야 합니다!", "qtext": "<strong>Q11. [호의 길이와 중심각 1]</strong><br>한 원에서 부채꼴의 호의 길이는 중심각의 크기에 어떻게 비례하는가?", "placeholder": "예: 정비례, 반비례", "error": "비례 원리 오류!", "ans_check": "ans === '정비례'", "hint": "부채꼴의 중심각이 커질 때 호의 길이도 이에 비례하여 일정하게 늘어나는 성질을 뜻합니다."},
    {"qnum": 12, "title": "태양 신의 석판 봉인", "story": "☀️ <strong>[호의 길이 비례식]</strong><br><br>중심각을 늘려서 석판을 더 많이 돌려야 합니다.", "qtext": "<strong>Q12. [호의 길이와 중심각 2]</strong><br>중심각이 40도일 때 호의 길이가 6cm라면, 중심각이 160도일 때 호의 길이를 구하시오.", "placeholder": "숫자만 입력", "error": "호의 길이 조절 실패!", "ans_check": "ans === '24'", "hint": "중심각의 크기와 호의 길이는 정비례하므로, 중심각이 4배 증가할 때 호의 길이도 똑같이 4배 증가합니다."},
    {"qnum": 13, "title": "태양 신의 석판 봉인", "story": "☀️ <strong>[부채꼴의 넓이 비율]</strong><br><br>빛을 모을 넓이의 비율을 맞추세요.", "qtext": "<strong>Q13. [부채꼴의 넓이와 중심각]</strong><br>부채꼴의 넓이가 원의 넓이의 1/6일 때, 이 부채꼴의 중심각의 크기를 구하시오.", "placeholder": "숫자만 입력", "error": "각도 조절 실패!", "ans_check": "ans === '60'", "hint": "원 전체의 중심각은 360도입니다. 넓이가 원의 1/6이므로 중심각도 360도의 1/6을 차지합니다."},
    {"qnum": 14, "title": "태양 신의 석판 봉인", "story": "☀️ <strong>[현의 성질]</strong><br><br>두 개의 열쇠 구멍의 길이가 같은지 확인합니다.", "qtext": "<strong>Q14. [현의 길이]</strong><br>중심각의 크기가 같은 두 부채꼴의 현의 길이는 서로 같은가?", "placeholder": "예: 같다, 다르다", "error": "현의 길이 오류!", "ans_check": "ans === '같다'", "hint": "중심각이 같은 두 부채꼴에서 원 위의 두 점을 곧게 이은 선분(현)의 길이를 비교해 봅니다."},
    {"qnum": 15, "title": "태양 신의 석판 봉인", "story": "☀️ <strong>[현과 중심각의 비례]</strong><br><br>비례 관계를 정확히 이해해야 다음으로 넘어갈 수 있습니다.", "qtext": "<strong>Q15. [현과 중심각의 비례]</strong><br>현의 길이는 중심각의 크기에 정비례하는가?", "placeholder": "예: 그렇다, 아니다", "error": "비례 관계 오류!", "ans_check": "ans === '아니다'", "hint": "중심각이 2배가 될 때 현의 길이도 정확히 2배가 되는지 원 위에 직접 그려 확인해 봅니다."},
    {"qnum": 16, "title": "최종 냉각 수조", "story": "🔑 <strong>[마지막 관문]</strong><br><br>드디어 수조 앞입니다! 수조의 덮개를 열려면 부채꼴 모양 청동 열쇠의 넓이와 둘레를 정확히 계산해야 합니다!", "qtext": "<strong>Q16. [원주 계산]</strong><br>반지름의 길이가 5cm인 원의 둘레의 길이를 구하시오. (원주율은 π, 입력시 '파이'로 기재)", "placeholder": "예: 5파이", "error": "둘레 계산 오류!", "ans_check": "ans === '10파이'", "hint": "반지름이 r인 원의 둘레 공식은 2 * 파이 * r 입니다."},
    {"qnum": 17, "title": "최종 냉각 수조", "story": "🔑 <strong>[청동 열쇠 호의 길이]</strong><br><br>청동 열쇠 테두리에 금실을 둘러야 합니다.", "qtext": "<strong>Q17. [호의 길이 계산]</strong><br>반지름의 길이가 9cm이고 중심각의 크기가 120도인 부채꼴의 호의 길이를 구하시오.", "placeholder": "예: 3파이", "error": "금실 길이 부족!", "ans_check": "ans === '6파이'", "hint": "반지름이 r, 중심각이 x도인 부채꼴 호의 길이 공식은 2 * 파이 * r * (x / 360) 입니다."},
    {"qnum": 18, "title": "최종 냉각 수조", "story": "🔑 <strong>[부채꼴 홈의 넓이]</strong><br><br>화강암 판 위에 에너지를 모을 면적을 계산하세요.", "qtext": "<strong>Q18. [부채꼴의 넓이 계산]</strong><br>반지름의 길이가 6cm이고 중심각의 크기가 60도인 부채꼴 모양 홈의 넓이를 구하시오.", "placeholder": "예: 2파이", "error": "면적 계산 오류!", "ans_check": "ans === '6파이'", "hint": "반지름이 r, 중심각이 x도인 부채꼴 넓이 공식은 파이 * r^2 * (x / 360) 입니다."},
    {"qnum": 19, "title": "최종 냉각 수조", "story": "🔑 <strong>[비상 게이트 수치]</strong><br><br>중심각을 모르는 상태에서 넓이를 계산해야 합니다.", "qtext": "<strong>Q19. [중심각 없이 넓이 구하기]</strong><br>반지름의 길이가 10cm이고 호의 길이가 5π cm인 부채꼴 모양 석문의 넓이를 계산하시오.", "placeholder": "예: 10파이", "error": "게이트 수치 오류!", "ans_check": "ans === '25파이'", "hint": "반지름 r과 호의 길이 l이 주어졌을 때의 부채꼴 넓이 공식인 (1/2) * r * l 을 활용합니다."},
    {"qnum": 20, "title": "최종 냉각 수조", "story": "🔑 <strong>[최종 탈출]</strong><br><br>마지막 암호 다이얼입니다! 색칠된 넓이를 맞추세요.", "qtext": "<strong>Q20. [색칠한 부분의 넓이]</strong><br>반지름이 8cm인 반원에서 반지름이 4cm인 반원 두 개를 뺀 색칠된 부분의 넓이를 구하시오.", "placeholder": "예: 12파이", "error": "다이얼이 잠겼습니다!", "ans_check": "ans === '16파이'", "hint": "반지름 8cm인 큰 반원 넓이에서 반지름 4cm인 작은 반원 두 개(합치면 작은 원 하나)의 넓이를 뺍니다."}
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
    q['hint'] = q.get('hint') or generate_hint(q['qtext'], q.get('ans_check', ''))

for q in qs:
    if 'hint' in q and '<button class="btn-hint"' not in q['qtext']:
        hint_text = q['hint'].replace("'", "\\'")
        q['qtext'] = q['qtext'].replace('</strong>', f'</strong> <button class="btn-hint" onclick="alert(\'💡 힌트: {hint_text}\')">💡 힌트</button>', 1)

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
            <img src="assets/m1_06_plane_geometry/q{qnum}.png" alt="Background" class="panel-image">
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
                <div class="story-text">여러분들이 땀을 흘리며 석문에 정답을 입력하고 다이얼을 돌리는 순간! 
                천장에서 쏟아지던 뜨겁고 살인적인 빛줄기가 마지막 거울에 반사되어 지하에 있는 깊은 냉각 수조의 중심부로 정확히 꽂힙니다. 
                쉭-! 하는 굉음과 함께 하얀 수증기가 신전을 가득 채우더니, 이내 굳게 닫혀 있던 탈출용 거대 돌벽이 스르륵 내려앉습니다. 
                눈을 뜰 수 없이 밝은 사막의 태양과 시원한 모래바람이 밀려옵니다. 거울 미궁 탈출에 성공했습니다!</div>
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
                        google.script.run.recordEnd(window.userRecordRow);
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


# We use regex to replace everything between the start of the first panel and <script> tag
import re
new_content = re.sub(r'<!-- Q1.*?<script>', lambda m: '<!-- Q1 -->\n' + panels_html + '\n        <script>', content, flags=re.DOTALL)

# And for JS:
new_content = re.sub(r'// Q1[\s\S]*?window\.onload = \(\) => \{', lambda m: '// Q1\n' + js_checks + '\n        window.onload = () => {', new_content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("App 06 updated successfully with regex.")
