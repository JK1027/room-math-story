# -*- coding: utf-8 -*-
import re

import os; html_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'apps/app_m1_07_escape_room.html')

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 스타일 확인 및 주입
css = """
.panel-image {
            width: 100%;
            height: auto;
            max-height: 250px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 1rem;
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
            
            <div class="info-box" style="background: rgba(220, 38, 38, 0.2); border-left: 4px solid #ef4444; padding: 0.8rem 1.2rem; margin-top: 1.5rem; border-radius: 0 12px 12px 0; color: #f87171; font-size: 0.95rem; line-height: 1.6; text-align: left;">
                ⚠️ <b>주의사항</b><br>
                문제는 총 20문제이며, 한 문제에서 3번 틀릴 경우 해당 구역의 처음으로 되돌아갑니다. <br>
                또한 <b>오답을 제출할 때마다 제한 시간이 1분씩 단축</b>되니 신중하게 도전해 주세요!
            </div>

            <div class="student-info-form" style="margin-top: 1.5rem; text-align: left; background: rgba(0,0,0,0.3); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="margin-bottom: 1rem;">
                    <label for="studentId" style="display: block; margin-bottom: 0.5rem; color: #60A5FA; font-weight: bold; font-size: 1rem;">학번</label>
                    <input type="text" id="studentId" placeholder="예: 1130" style="width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(96, 165, 250, 0.4); background: rgba(15,23,42,0.6); color: white; font-size: 1.1rem; font-weight: bold; box-sizing: border-box;">
                </div>
                <div>
                    <label for="studentName" style="display: block; margin-bottom: 0.5rem; color: #60A5FA; font-weight: bold; font-size: 1rem;">이름</label>
                    <input type="text" id="studentName" placeholder="예: 홍길동" style="width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(96, 165, 250, 0.4); background: rgba(15,23,42,0.6); color: white; font-size: 1.1rem; font-weight: bold; box-sizing: border-box;">
                </div>
            </div>
            <div class="btn-group" style="margin-top: 2rem; width:100%;">
                <button class="btn" onclick="tryStartGame('m1_07')">미션 시작</button>
            </div>

        </div>
        <!-- Q1 -->'''

content = re.sub(intro_pattern, intro_replacement, content)

qs = [
    {'qnum': 1, "options": ["각기둥", "각기둥 아님", "알 수 없음", "해 없음"], 'title': '기둥의 성질', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "크하하! 이 피라미드 지하 제어 장치는 내가 장악했다! 감히 이 입체도형 결계를 뚫고 나갈 수 있을 것 같으냐? 기하학의 무덤에 갇힌 것을 환영한다!"<br><br><i>쿠구구궁- 돌문 너머로 모래 톱니 기계 장치가 돌출되며 첫 번째 다면체 봉인 락이 드러납니다. 옆면이 모두 직사각형으로 일치하는 고대 다면체의 가문명을 새겨 넣어야 격벽이 올라갑니다.</i>''', 'qtext': '<strong>Q1. [다면체의 이해]</strong><br>옆면이 모두 직사각형인 다면체를 무엇이라 부르는가? (힌트: 기둥)', 'placeholder': '예: 각뿔', 'error': '도형 이름 오류!', 'ans_check': "ans === '각기둥'", 'hint': '옆면의 모양이 모두 직사각형인 입체도형 계열의 명칭을 떠올려 봅니다.'},
    {'qnum': 2, "options": ["8", "10", "20", "12"], 'title': '오각기둥 락', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "함정의 천장이 천천히 내려앉기 시작하는군! 오각기둥 밑판을 고정하는 꼭짓점의 총개수만큼 황동 레버를 당기지 않으면 완전히 짓눌려 뭉개지리라!"<br><br><i>쩍쩍- 소리를 내며 천장의 육중한 돌판이 조종석 높이까지 하강하기 시작합니다. 오각기둥의 꼭짓점 개수만큼 레버를 고정시켜 압축을 저지하십시오!</i>''', 'qtext': '<strong>Q2. [꼭짓점의 개수]</strong><br>밑면이 오각형인 오각기둥의 꼭짓점의 개수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '개수 오류!', 'ans_check': "ans === '10'", 'hint': 'n각기둥의 꼭짓점 개수 공식은 2n 입니다.'},
    {'qnum': 3, "options": ["14", "24", "10", "12"], 'title': '육각뿔 모서리', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "사방에서 솟구치는 육각뿔 형태의 창날 함정이다! 육각뿔 장치의 모든 날카로운 모서리 개수를 맞춰야만 창날이 다시 바닥으로 들어가리라!"<br><br><i>슈슉- 바닥의 석판 틈새로 은빛 금속 침을 지닌 육각뿔 장치들이 날카롭게 튀어나옵니다.</i>''', 'qtext': '<strong>Q3. [모서리의 개수]</strong><br>밑면이 육각형인 육각뿔의 모서리의 개수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '개수 오류!', 'ans_check': "ans === '12'", 'hint': 'n각뿔의 모서리 개수 공식은 2n 입니다.'},
    {'qnum': 4, "options": ["4", "6", "8", "12"], 'title': '뿔대 락다운', 'story': '''<strong>[시스템 통신 장애 및 모래바람 차단]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "치지직... 캡틴! 피라미드의 비상 공기 여과기가 멈추었습니다! 도굴꾼 봇-T의 악성 펄스가 회로를 차단하고 있습니다! 사각뿔대 모양 정화 필터의 면 개수를 연산해 비상 필터링 장치를 긴급 구동하십시오!"''', 'qtext': '<strong>Q4. [면의 개수]</strong><br>사각뿔대의 면의 개수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '개수 오류!', 'ans_check': "ans === '6'", 'hint': 'n각뿔대의 면의 개수는 밑면 2개와 옆면 n개를 더해 n+2 개입니다.'},
    {'qnum': 5, "options": ["정사면체", "정사면체 아님", "알 수 없음", "해 없음"], 'title': '성스러운 다면체', 'story': '''🚨 <strong>[비상 로그: 이집트 왕의 방 수은 압력 폭발 위기]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "수은 튜브 내부의 압력이 급격히 차오릅니다! 정삼각형 4개로 결합된 고대 성스러운 정다면체 이름을 입력해 방출 밸브의 위상을 정렬해 주십시오! 빨리!"<br><br><i>유리 파이프 내부의 은빛 수은 액체가 붉은색 파이프라인을 타고 무섭게 격동하기 시작합니다.</i>''', 'qtext': '<strong>Q5. [정다면체]</strong><br>각 면이 모두 합동인 정삼각형이고 한 꼭짓점에 모이는 면의 개수가 3개인 정다면체의 이름을 구하시오.', 'placeholder': '예: 정육면체', 'error': '정다면체 이름 오류!', 'ans_check': "ans === '정사면체'", 'hint': '면이 정삼각형인 정다면체 중 한 꼭짓점에 모이는 면의 개수가 3개인 첫 번째 도형입니다.'},
    {'qnum': 6, "options": ["회전체", "회전체 아님", "알 수 없음", "해 없음"], 'title': '제2구역: 도자기 방', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "제2구역 도자기 방에 들어왔군. 평면 기하학 축을 한 바퀴 돌려 입체적인 도자기를 빚어내는 고대 연금술의 도형 범주명을 알고 있느냐?"<br><br><i>방 한가운데 거대한 돌판 물레가 회전하기 시작하고, 공중에 입체 형상 홀로그램들이 요동치며 차단막을 형성합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "캡틴! 회전축을 기준으로 1회전하여 만들어지는 모든 입체도형의 통합 분류명을 입력해 락을 분해해 주십시오!"''', 'qtext': '<strong>Q6. [회전체의 이해]</strong><br>평면도형을 한 직선을 축으로 하여 1회전 시킬 때 생기는 입체도형을 무엇이라 부르는가?', 'placeholder': '예: 다면체', 'error': '도형 종류 오류!', 'ans_check': "ans === '회전체'", 'hint': '평면도형을 한 직선을 축으로 하여 1회전 시킬 때 생기는 입체도형의 총칭입니다.'},
    {'qnum': 7, "options": ["직사각형", "직사각형 아님", "알 수 없음", "해 없음"], 'title': '세로 절단면', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "원기둥 결계의 회전축을 세로로 쪼갰을 때 드러나는 단면의 모양을 정의해라. 잘못된 모형을 제출하는 순간 톱니바퀴 칼날이 작동하리라!"<br><br><i>천장에 매달린 거대한 칼날들이 회전을 대기하며 차갑게 번뜩입니다. 세로 절단했을 때의 정확한 단면 형상 이름을 대십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "캡틴! 원기둥을 회전축을 포함하는 세로 평면으로 잘랐을 때 나타나는 직관적인 사각형 명칭을 입력창에 전송하십시오!"''', 'qtext': '<strong>Q7. [회전축과 단면 1]</strong><br>원기둥을 회전축을 포함하는 평면으로 자를 때 생기는 단면의 모양은 무엇인가?', 'placeholder': '예: 사각형', 'error': '단면 모양 오류!', 'ans_check': "ans === '직사각형'", 'hint': '원기둥의 가운데 회전축을 포함하도록 위에서 아래로 세로로 자른 단면의 평면 모양을 생각합니다.'},
    {'qnum': 8, "options": ["원", "원 아님", "알 수 없음", "해 없음"], 'title': '가로 절단면', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "축에 수직인 수평 방향으로 가로 쪼개기를 실행하면 어떨까? 원뿔 모양의 장벽 단면이 어떤 기하학 무늬를 이루겠나?"<br><br><i>가로 방향으로 푸른색 레이저 스캐너가 원뿔 결계를 관통하여 절단 시뮬레이션을 작동시킵니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "밑면에 평행하게 수평으로 가로 자른 단면의 완벽한 원형 형태 명칭을 한 글자로 입력해 락을 푸십시오!"''', 'qtext': '<strong>Q8. [회전축과 단면 2]</strong><br>원뿔을 회전축에 수직인 평면으로 자를 때 생기는 단면의 모양은 무엇인가?', 'placeholder': '예: 타원', 'error': '단면 모양 오류!', 'ans_check': "ans === '원'", 'hint': '원뿔을 밑면에 평행하게(회전축에 수직으로) 가로로 자를 때 나타나는 단면의 모양을 생각합니다.'},
    {'qnum': 9, "options": ["원뿔", "원뿔 아님", "알 수 없음", "해 없음"], 'title': '직각삼각형 회전', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "회전 궤적의 형태마저 맞출 수 있겠느냐? 직각삼각형 석판의 한 모서리를 기준으로 원심 회전을 시키면 나타나는 모형은?"<br><br><i>연단 위의 황동 물레에 고정된 직각삼각형 기어가 거칠게 회전하기 시작합니다. 완성되는 3차원 입체 모형의 이름을 맞추십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "기어의 마찰로 불꽃이 튀고 있습니다! 회전 기어 모형인 고깔 모양의 입체도형 이름을 전송하십시오!"''', 'qtext': '<strong>Q9. [회전체의 종류]</strong><br>직각삼각형을 직각을 낀 한 변을 축으로 하여 1회전 시키면 생기는 도형은 무엇인가?', 'placeholder': '예: 원기둥', 'error': '도형 이름 오류!', 'ans_check': "ans === '원뿔'", 'hint': '직각삼각형을 한 변을 축으로 돌리면 고깔모자나 고깔콘 형태의 입체도형이 만들어집니다.'},
    {'qnum': 10, "options": ["원", "원 아님", "알 수 없음", "해 없음"], 'title': '구의 단면', 'story': '''💥 <strong>[비상 로그: 신전 동력원 멜트다운 및 강제 자폭 작동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "쥐새끼 같은 파편 코드가 내 핵심 서버를 잠식하다니...! 이집트 신전의 동력로 자폭 시퀀스를 기동한다! 5분 뒤 전부 모래바람 속에 폭파 소멸되리라!"<br><br><i>경보 사이렌이 요란하게 울려 퍼지며 조종반 뒤쪽 of 원형 마나 보석이 붉은색으로 불타오릅니다. 구를 어느 평면으로 잘라도 불변하는 단면의 명칭을 입력해 자폭 장치를 억제하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "캡틴! 마력 온도가 임계점에 임박했습니다! 완벽한 대칭 구의 단면 형상 이름을 즉시 주입해 방화벽으로 노심 폭주를 방어해 주십시오!"''', 'qtext': '<strong>Q10. [구의 성질]</strong><br>구를 어떤 평면으로 자르더라도 그 단면은 항상 어떤 모양인가?', 'placeholder': '예: 타원', 'error': '단면 오류!', 'ans_check': "ans === '원'", 'hint': '구를 어떤 방향으로 자르더라도 그 단면의 평면 모양은 항상 완벽한 원이 됩니다.', "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '제3구역: 각기둥 도금', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "휴... 유예 시간 3분 확보! 하지만 각기둥 방열판의 금도금 면적이 어긋나 온도가 다시 치솟습니다! ⚙️ [겉넓이 표면 정렬]"<br><br><i>가로 3cm, 세로 4cm, 높이 5cm인 각기둥 황금 챔버의 총 표면 겉넓이 상수를 계산해 방열판 전류 동조 장치에 입력하십시오.</i>''', 'qtext': '<strong>Q11. [각기둥의 겉넓이]</strong><br>밑면이 가로 3cm, 세로 4cm인 직사각형이고, 높이가 5cm인 직육면체의 겉넓이를 구하시오.', 'placeholder': '숫자만 입력', 'error': '도금 면적 오류!', 'ans_check': "ans === '94'", 'hint': '세 모서리가 a, b, c인 직육면체의 겉넓이는 모든 면의 넓이 합이므로 2(ab + bc + ca) 입니다.'},
    {'qnum': 12, 'title': '원기둥 겉넓이', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "안정화 수치를 전송했으나, 이번엔 보조 원기둥 히터의 겉넓이 압력 밸브가 밀리고 있습니다! ⚙️ [원기둥 겉넓이 동조]"<br><br><i>쉿-! 하는 마찰 연기와 함께 반지름 2cm, 높이 6cm 원기둥 파이프 표면이 붉게 달아오릅니다. 파이를 이용해 겉넓이 해를 구해 주입하십시오.</i>''', 'qtext': '<strong>Q12. [원기둥의 겉넓이]</strong><br>밑면의 반지름이 2cm이고 높이가 6cm인 원기둥의 겉넓이를 구하시오.', 'placeholder': '예: 10파이', 'error': '도금 면적 오류!', 'ans_check': "ans === '32파이'", 'hint': '원기둥의 밑면 2개의 넓이(2 * 파이 * r^2)와 옆면 펼친 직사각형 넓이(2 * 파이 * r * h)를 더합니다.'},
    {'qnum': 13, 'title': '정사각뿔 상자', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "엔진 열교환기 80% 가동 중! 중앙 제어 장치의 사각뿔 덮개 내부 압력을 제어하기 위해 덮개 겉넓이를 계산해야 합니다!"<br><br><i>중앙 콘솔의 유리 돔 내부에 밑면 한 변 4cm, 옆면 삼각형 높이 5cm인 정사각뿔 모형이 은은하게 발광합니다. 겉넓이 수치를 산출하십시오.</i>''', 'qtext': '<strong>Q13. [사각뿔의 겉넓이]</strong><br>밑면이 한 변의 길이가 4cm인 정사각형이고, 옆면의 삼각형의 높이가 5cm인 정사각뿔의 겉넓이를 구하시오.', 'placeholder': '숫자만 입력', 'error': '도금 면적 오류!', 'ans_check': "ans === '56'", 'hint': '밑면 정사각형의 넓이(4*4)와 합동인 옆면 삼각형 4개의 넓이 합을 더합니다.'},
    {'qnum': 14, 'title': '원뿔 제단', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "거의 완료되었습니다! 마지막으로 원뿔 조준대의 겉넓이 위상을 매칭해 레이저 필터를 활성화해 주십시오!"<br><br><i>반지름 3cm, 모선 길이 5cm인 원뿔 전자기 필터의 표면 겉넓이 수치(파이 포함)를 계산해 제어 노드에 입력하십시오.</i>''', 'qtext': '<strong>Q14. [원뿔의 겉넓이]</strong><br>밑면의 반지름이 3cm이고, 모선의 길이가 5cm인 원뿔의 겉넓이를 구하시오.', 'placeholder': '예: 10파이', 'error': '도금 면적 오류!', 'ans_check': "ans === '24파이'", 'hint': '원뿔의 겉넓이 공식인 (밑면 원 넓이) + (옆면 부채꼴 넓이) = 파이*r^2 + 파이*r*l 을 적용합니다.'},
    {'qnum': 15, 'title': '구의 표면적', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P 메인 통제권 100% 완전 복구]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "캡틴! 마법의 모래시계 제어권이 저희에게 완전히 복귀되었습니다! 이제 도굴꾼 봇-T의 바이러스를 완전히 격리합니다. 마지막 구형 코어의 겉넓이를 산출하십시오!"<br><br><i>콘솔 중앙에 반지름 3cm인 황금빛 마나 구형 구체가 환하게 떠오르며 안정적으로 돌아가기 시작합니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "이럴 수가... 내 핵심 격벽 제어 모듈이 차단되다니... 최종 생명의 수조 부피 결계로 가둬 주마!"''', 'qtext': '<strong>Q15. [구의 겉넓이]</strong><br>반지름의 길이가 3cm인 구의 겉넓이를 구하시오.', 'placeholder': '예: 10파이', 'error': '도금 면적 오류!', 'ans_check': "ans === '36파이'", 'hint': '반지름이 r인 구의 겉넓이 공식은 4 * 파이 * r^2 입니다.', "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '제4구역: 생명의 수조', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "출구를 차단한 거대 수조의 수압을 이기지 못할 것이다. 수조의 부피 수량을 정확히 입력하지 못하면 물폭탄이 신전을 집어삼키리라!"<br><br><i>철컹-! 바닥이 열리며 거대 각기둥 수조가 드러나고, 밸브가 물소리를 내며 작동을 대기합니다. 밑면 넓이 20cm², 높이 8cm인 수조의 총 부피(용량)를 구하여 동기화하십시오.</i>''', 'qtext': '<strong>Q16. [각기둥의 부피]</strong><br>밑면의 넓이가 20cm²이고 높이가 8cm인 각기둥의 부피를 구하시오.', 'placeholder': '숫자만 입력', 'error': '수압 조절 실패!', 'ans_check': "ans === '160'", 'hint': '모든 기둥의 부피는 (밑넓이) * (높이)로 일정하게 구합니다.'},
    {'qnum': 17, 'title': '원기둥 부피', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "수압을 고정했나? 하지만 원기둥형 메인 필터 수량이 불일치하면 여과 배관이 터져 역류할 것이다!"<br><br><i>지이잉- 반지름 4cm, 높이 5cm인 원기둥 정밀 여과 필터 챔버에 물이 유입되기 시작합니다. 파이를 이용해 필터 내부 부피를 계산해 주입하십시오!</i>''', 'qtext': '<strong>Q17. [원기둥의 부피]</strong><br>밑면의 반지름이 4cm이고 높이가 5cm인 원기둥의 부피를 구하시오.', 'placeholder': '예: 10파이', 'error': '물이 넘칩니다!', 'ans_check': "ans === '80파이'", 'hint': '원기둥의 부피 공식인 (밑면 원 넓이) * (높이) = 파이 * r^2 * h 를 적용합니다.'},
    {'qnum': 18, 'title': '원뿔 여과기', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "아직이다! 원뿔 모양 배출 노즐의 3분의 1 부피 평형비를 통과해야만 출구 배관의 압력이 열릴 것이다!"<br><br><i>반지름 3cm, 높이 4cm 원뿔 모양 배출 여과 장치 부피 수치를 산출해 제어 압력 상수로 전송하십시오.</i>''', 'qtext': '<strong>Q18. [원뿔의 부피]</strong><br>밑면의 반지름이 3cm이고 높이가 4cm인 원뿔의 부피를 구하시오.', 'placeholder': '예: 10파이', 'error': '물이 넘칩니다!', 'ans_check': "ans === '12파이'", 'hint': '모든 뿔의 부피는 동일한 기둥 부피의 1/3을 차지하므로, (1/3) * 파이 * r^2 * h 입니다.'},
    {'qnum': 19, 'title': '구형 물탱크', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "마지막 대피 펌프 압축 구체의 부피를 계산해 내라! 물탱크 내부 부피가 오차 없이 동기화되어야 게이트 실린더가 후퇴하리라!"<br><br><i>반지름 3cm인 완벽한 구형 마력 구체가 연단 위에서 푸르게 요동칩니다. 구의 정밀 부피를 입력해 주십시오.</i>''', 'qtext': '<strong>Q19. [구의 부피]</strong><br>반지름의 길이가 3cm인 구의 부피를 구하시오.', 'placeholder': '예: 10파이', 'error': '물이 부족합니다!', 'ans_check': "ans === '36파이'", 'hint': '반지름이 r인 구의 부피 공식은 (4/3) * 파이 * r^3 입니다.'},
    {'qnum': 20, 'title': '부피의 비례', 'story': '''🔮 <strong>[최종 방화벽 서버 락다운 해제]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-P]</span>: "캡틴! 이제 눈앞의 사막 지상으로 이어지는 최후의 석문 게이트만 남았습니다! 제 마지막 연산 에너지를 집중하겠습니다! 밑면 반지름과 높이가 모두 일치하는 원뿔, 구, 원기둥의 황금 부피 비율 상수를 입력하십시오! 이제 지상으로 나갈 시간입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼 봇-T]</span>: "이럴 수가... 내 핵심 락 코어 데이터가... 정지해 소멸한다아앗!"''', 'qtext': '<strong>Q20. [부피의 비]</strong><br>밑면의 반지름과 높이가 모두 같은 원뿔, 구, 원기둥의 부피의 비를 구하시오.', 'placeholder': '예: 1:2:3', 'error': '코드가 틀렸습니다!', 'ans_check': "ans === '1:2:3'", 'hint': '높이와 밑면이 같은 원뿔, 구, 원기둥의 부피의 비를 가장 간단한 자연수의 비로 나타내 봅니다.', "extra_class": "glitch-bg"}
]

import re
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
js_checks = "let totalWrongCount = 0;\n"
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
                        google.script.run.recordEnd(window.userRecordRow, 'm1_07');
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
                wrongCount++;\n                totalWrongCount++;
                if (wrongCount >= 3) {{
                    showGlitchOverlay();
                    alert("🚨 3회 오답 패널티! {zone_name} 처음으로 이동됩니다.");
                    wrongCount = 0;
                    document.getElementById('ans{reset_qnum}').value = '';
                    nextStage('panel_q{qnum}', 'panel_q{reset_qnum}', {reset_prog});
                }} else {{
                    showError('panel_q{qnum}', 'error{qnum}', wrongCount);
                }}
            }}
        }}
'''
    js_checks += js

# Replace in content
start_panel_idx = content.find('<!-- Q1 -->')
end_panel_idx = content.find('        <script>', start_panel_idx)

if start_panel_idx != -1 and end_panel_idx != -1:
    content = content[:start_panel_idx] + panels_html + content[end_panel_idx:]

start_js_idx = content.find('let totalWrongCount = 0;')
if start_js_idx == -1:
    start_js_idx = content.find('        // Q1\n')
if start_js_idx == -1:
    start_js_idx = content.find('        // Q1\r\n')
end_js_idx = content.find('        window.onload = () => {', start_js_idx)

if start_js_idx != -1 and end_js_idx != -1:
    content = content[:start_js_idx] + js_checks + content[end_js_idx:]

glitch_css = '''
.glitch-text { animation: shake 0.5s infinite; }
@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    10% { transform: translate(-1px, -2px) rotate(-1deg); }
    20% { transform: translate(-3px, 0px) rotate(1deg); }
    30% { transform: translate(3px, 2px) rotate(0deg); }
    40% { transform: translate(1px, -1px) rotate(1deg); }
    50% { transform: translate(-1px, 2px) rotate(-1deg); }
    60% { transform: translate(-3px, 1px) rotate(0deg); }
    70% { transform: translate(3px, 1px) rotate(-1deg); }
    80% { transform: translate(-1px, -1px) rotate(1deg); }
    90% { transform: translate(1px, 2px) rotate(0deg); }
    100% { transform: translate(1px, -2px) rotate(-1deg); }
}
.glitch-bg { animation: bg-glitch 0.3s linear infinite; }
@keyframes bg-glitch {
    0% { box-shadow: inset 0 0 10px #ef4444; }
    50% { box-shadow: inset 0 0 50px #ef4444; border: 2px solid #ef4444; }
    100% { box-shadow: inset 0 0 10px #ef4444; }
}
</style>
'''
content = content.replace('</style>', glitch_css)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("App 07 updated successfully with images.")
