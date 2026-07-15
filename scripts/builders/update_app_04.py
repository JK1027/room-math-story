import re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_04_escape_room.html")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# ----------------- 올바른 이미지 매핑 테이블 정의 -----------------
img_map = {
    1: 'img1_radar.png',
    2: 'img1_radar.png',
    3: 'img1_radar.png',
    4: 'img11_deep_cave.png',
    5: 'img2_pillars.png',
    6: 'img3_atlantis.png',
    7: 'img12_compass.png',
    8: 'img3_atlantis.png',
    9: 'img4_mirror.png',
    10: 'img4_mirror.png',
    11: 'img5_descend.png',
    12: 'img13_graph_speed.png',
    13: 'img6_oxygen.png',
    14: 'img6_oxygen.png',
    15: 'img14_oxygen_leak.png',
    16: 'img7_gears.png',
    17: 'img7_gears.png',
    18: 'img8_buoyancy.png',
    19: 'img15_golden_door.png',
    20: 'img9_laser.png',
    'outro': 'img10_escape.png',
    'intro': 'img1_radar.png'
}

# ----------------- 리소스 데이터 정의 (어드벤처 버전 톤앤매너 변경) -----------------
# 자바스크립트 내 따옴표 충돌 방지를 위해 속성값에 작은따옴표만 사용
nereus = "<span style='color: #60a5fa; text-shadow: 0 0 5px #3b82f6;'>[네레우스]</span>"
poseidon = "<span class='glitch-text' style='color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;'>[포세이돈-V]</span>"
dyn_captain = "<span class='dynamic-captain-name'>캡틴</span>"

qs = [
    {"qnum": 1, "title": "심해로 가는 좌표 (순서쌍과 좌표)", "story": f"🌊 <strong>[진입 투하 축 설정]</strong><br><br>{poseidon}: \"멈춰라, 외부인! 수학의 기본인 좌표도 모르는 자가 감히 아틀란티스의 문을 두드리는가? 자격을 증명해라!\"<br><br>🚨 <strong>[수문장의 방해 감지]</strong><br><br>{nereus}: \"으아앗, {dyn_captain}! 전설의 수문장 AI입니다! 생각보다 너무 깐깐해요. 제발 저 순서쌍 퀴즈 좀 맞춰서 통과하게 해주세요!\"", "qtext": "<strong>Q1. [순서쌍 좌표 찍기]</strong><br>x좌표가 -5 이고, y좌표가 8 인 점의 <strong>좌표</strong>를 순서쌍 기호 괄호 ()를 사용하여 나타내시오.", "placeholder": "예: (3, 4)", "error": "투하 궤적이 정렬되지 않아 선체가 조류에 흔들립니다!", "ans_check": "ans === '-5,8'"},
    {"qnum": 2, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[날개 수평 정렬]</strong><br><br>{poseidon}: \"겨우 진입각만 맞춘 주제에 뻐기지 마라! 쇄도하는 해류는 어찌 피할 텐가? 추진용 수직 보조 날개(y축)를 중립(y=0)으로 잠그고, 수평 제어각(x축)만 7도 전개하는 좌표 신호를 입력해 보아라!\"", "qtext": "<strong>Q2. [x축, y축 위의 점]</strong><br>x축 위에 있고 x좌표가 7인 점의 좌표를 나타내시오.", "placeholder": "예: (2, 0)", "error": "수평 보조 밸브 고장! 수압 경고등이 켜집니다!", "ans_check": "ans === '7,0'"},
    {"qnum": 3, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[영점 조준 복원]</strong><br><br>{nereus}: \"{dyn_captain}! 저 수문장이 자꾸 훼방을 놓아서 영점 조준 회로가 흔들리고 있습니다! 수평과 수직의 평형이 완벽히 만나는 물리적 '원점' 좌표를 빠르게 인증하여 영점을 꽉 잡아주십시오!\"", "qtext": "<strong>Q3. [원점의 좌표]</strong><br>두 좌표축이 만나는 원점 O의 좌표를 나타내시오.", "placeholder": "예: (x, y)", "error": "영점 동기화 실패! 자이로 센서가 빙글빙글 돕니다!", "ans_check": "ans === '0,0'"},
    {"qnum": 4, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[수직 동굴 강하]</strong><br><br>{poseidon}: \"원점 조율이라니, 하찮은 발악이군. 전방의 해저 낭떠러지를 통과하기 위해 수평 기어는 완전 중립(x=0)으로 락하고, 수직 강하 장치(y축)의 파워를 -3으로 밀어 넣어라. 오차가 생기면 벽에 쿵! 이다!\"", "qtext": "<strong>Q4. [좌표 평면 위의 점]</strong><br>y축 위에 있고 y좌표가 -3인 점의 좌표를 나타내시오.", "placeholder": "예: (0, -5)", "error": "수직 제어가 늦어 절벽에 부딪힐 뻔했습니다!", "ans_check": "ans === '0,-3'"},
    {"qnum": 5, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[소용돌이 차단벽]</strong><br><br>{nereus}: \"{dyn_captain}! 수호 기계들이 네 개의 에너지 포인트 기둥으로 사각형 소용돌이 결계를 구축했습니다. 이 차단막의 넓이를 정확하게 구해야 펄스 방출로 뚫고 나갈 수 있습니다!\"", "qtext": "<strong>Q5. [도형의 넓이]</strong><br>좌표평면 위에 네 기둥 A(3, 4), B(-3, 4), C(-3, -4), D(3, -4)를 이은 직사각형의 넓이를 구하시오.", "placeholder": "숫자만 입력", "error": "차단벽 넓이 연산 오류! 잠수정이 튕겨 나옵니다!", "ans_check": "ans === '48'"},
    {"qnum": 6, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[제1 격자 방어망]</strong><br><br>{poseidon}: \"결계를 넘다니 제법이군. 하지만 고대 기하학 사분면 방어 격자가 기동하면 어떨까? 우리 도시의 기동점 좌표 (2, -5)가 관리하는 사분면 격자 영역을 추적하라!\"", "qtext": "<strong>Q6. [사분면의 부호 1]</strong><br>점 (2, -5)는 제 몇 사분면 위의 점인가?", "placeholder": "선택지를 골라주세요", "options": ["제1사분면", "제2사분면", "제3사분면", "제4사분면"], "error": "잘못된 방어망 탐색! 빙글빙글 돌아갑니다.", "ans_check": "ans === '제4사분면'"},
    {"qnum": 7, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[제2 격자 방어망]</strong><br><br>{poseidon}: \"호오, 아직 포기하지 않았군. 그렇다면 제어 좌표 (-4, -7)가 가리키는 사분면 위상은 어디인지 판독해라. 틀리면 에너지가 훅훅 줄어들 거다!\"", "qtext": "<strong>Q7. [사분면의 부호 2]</strong><br>점 (-4, -7)은 제 몇 사분면 위의 점인가?", "placeholder": "선택지를 골라주세요", "options": ["제1사분면", "제2사분면", "제3사분면", "제4사분면"], "error": "사분면 위상 동조 실패! 회로가 삐걱거립니다.", "ans_check": "ans === '제3사분면'"},
    {"qnum": 8, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[암호화 부호 논리]</strong><br><br>{nereus}: \"{dyn_captain}! 포세이돈이 좌표 P(a, b)의 부호 조건을 꼬아놨습니다! a × b < 0 이고 a - b > 0 일 때 논리적인 부호 조합을 판별하여 P의 정확한 사분면 구역을 풀어주십시오!\"", "qtext": "<strong>Q8. [사분면의 이해]</strong><br>점 P(a, b)에 대하여 a × b < 0 이고 a - b > 0 일 때, 점 P는 제 몇 사분면 위에 있는지 구하시오.", "placeholder": "예: 4 또는 제4사분면", "error": "부호 판별 불일치! 모듈이 달아오릅니다.", "ans_check": "ans === '4' || ans.includes('제4') || ans.includes('4사')"},
    {"qnum": 9, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[역 위상 연산]</strong><br><br>{poseidon}: \"조력자 녀석이 제법 똑똑하구나. 하지만 내 암호 폭격을 버틸 수 있을까? 본래 2사분면에 존재하던 점 P(a, b)의 대칭점 Q(a, -b)가 가리키는 사분면은 어디인가!\"", "qtext": "<strong>Q9. [사분면의 응용 1]</strong><br>점 P(a, b)가 제2사분면 위의 점일 때, 점 Q(a, -b)는 제 몇 사분면 위의 점인가?", "placeholder": "선택지를 골라주세요", "options": ["제1사분면", "제2사분면", "제3사분면", "제4사분면"], "error": "신호 대칭 불일치! 펌프가 덜컹거립니다.", "ans_check": "ans === '제3사분면'"},
    {"qnum": 10, "title": "아틀란티스의 사분면 결계", "story": f"💥 <strong>[긴급 상황: 외부 선체 흔들림!]</strong><br><br>{poseidon}: \"방어 그리드 최종 활성화! 좌표 Q(-a, b)의 사분면을 계산하지 못하면 쫓아내주마! 집으로 돌아가라!\"<br><br>{nereus}: \"{dyn_captain}! 포세이돈이 장난을 멈출 생각이 없나 봐요! 방어막 에너지가 닳고 있어요. 빨리 마지막 부호를 계산해 주세요!\"<br><br><div id='choice-container-q10' style='margin-top: 1rem; display: flex; gap: 1rem;'><button class='btn btn-secondary' onclick='makeChoiceQ10(1); event.stopPropagation();'>⚡ 발전기 오버클록</button><button class='btn btn-secondary' onclick='makeChoiceQ10(2); event.stopPropagation();'>🛡️ 방어막 과부하 전개</button></div><div id='chosen-story-q10' style='display: none; margin-top: 1rem;'></div>", "qtext": "<strong>Q10. [사분면의 응용 2]</strong><br>점 P(a, b)가 제3사분면 위의 점일 때, 점 Q(-a, b)는 제 몇 사분면 위의 점인가?", "placeholder": "예: 4 또는 제4사분면", "error": "잘못된 구역입니다!", "ans_check": "ans === '4' || ans.includes('제4') || ans.includes('4사')", "extra_class": "glitch-bg"},
    {"qnum": 11, "title": "해저 수압의 변화", "story": f"🌊 <strong>[이동 상태 그래프 분석]</strong><br><br>{poseidon}: \"단순한 좌표 찍기는 유치원생도 하지. 진정한 아틀란티스인은 그래프의 흐름을 읽는 법! 수평을 유지한 이 구간이 뜻하는 건 뭘까? 과연 이 변화량을 꿰뚫어 볼 수 있을까?\"", "qtext": "<strong>Q11. [그래프 해석 1]</strong><br>x분 동안 이동한 거리 y m를 나타낸 그래프가 수평을 유지한 구간은 잠수정이 무엇을 의미하는가?", "placeholder": "예: 상승, 하강, 정지", "error": "상태 해석 불일치! 다시 생각해봐라!", "ans_check": "ans === '정지'"},
    {"qnum": 12, "title": "해저 수압의 변화", "story": f"🌊 <strong>[정비례 강하 압력]</strong><br><br>{nereus}: \"급속 강하 장치의 압력이 변하고 있습니다! 일정한 속도로 내려가 수심 100m까지 10분 소요되었다면, 정확히 5분이 경과한 시점의 수심을 재빨리 구하여 컨트롤 장치를 갱신해 주십시오!\"", "qtext": "<strong>Q12. [그래프 해석 2]</strong><br>잠수정이 수심 100m까지 10분 동안 일정한 속력으로 내려갔다. 5분일 때 수심은 몇 m인가?", "placeholder": "숫자만 입력", "error": "보간 연산 오류! 유압 계통이 윙윙거립니다.", "ans_check": "ans === '50'"},
    {"qnum": 13, "title": "해저 수압의 변화", "story": f"🌊 <strong>[라이벌 의식과 두뇌 대결]</strong><br><br>{poseidon}: \"원점을 지나는 우상향 정비례 직선에서, 독립변수 x가 늘어날 때 y는 어떻게 될까? 이것도 모르면 심해의 보물을 차지할 자격이 없다!\"<br><br>{nereus}: \"우리 {dyn_captain}을 무시하지 마십시오! 우상향인지 우하향인지 우리가 더 잘 안다는 걸 보여줍시다!\"", "qtext": "<strong>Q13. [그래프 해석 3]</strong><br>그래프가 원점을 지나는 우상향 직선일 때, x가 증가하면 y는 어떻게 되는가?", "placeholder": "선택지를 골라주세요", "options": ["증가한다", "감소한다", "변하지 않는다"], "error": "출력 증감 판단 오류! 똑바로 보아라!", "ans_check": "ans === '증가한다'"},
    {"qnum": 14, "title": "해저 수압의 변화", "story": f"🌊 <strong>[기어 정지 잔량]</strong><br><br>{nereus}: \"수심 100m 지점에 5분간 완전히 정체해 있었을 때의 물리적 깊이 변화량 y값을 레지스터에 전송하십시오! 거의 다 왔습니다!\"", "qtext": "<strong>Q14. [그래프 해석 4]</strong><br>수심 100m에서 5분간 머물렀다. 이 5분 동안 깊이 y값의 변화량은 얼마인가?", "placeholder": "숫자만 입력", "error": "변화량 오차 감지! 기어 동조가 안 됩니다.", "ans_check": "ans === '0'"},
    {"qnum": 15, "title": "해저 수압의 변화", "story": f"🚨 <strong>[산소 챔버 퀴즈]</strong><br><br>{poseidon}: \"산소 밸브가 말썽이군! 시간이 흐름에 따라 남은 산소량이 줄어드는 그래프 개형이 우상향인지 우하향인지 맞춰봐라! 맞춰야만 밸브가 열릴 거다!\"", "qtext": "<strong>Q15. [변수 관계 이해]</strong><br>시간 x가 지남에 따라 남은 산소량 y를 그래프로 그리면, 우하향하는 모양인가 우상향하는 모양인가?", "placeholder": "선택지를 골라주세요", "options": ["우상향하는 모양", "우하향하는 모양", "수평인 모양"], "error": "산소 예측 밸브 고착! 숨을 참아야 할지도 몰라요!", "ans_check": "ans === '우하향하는 모양'", "extra_class": "glitch-bg"}
]

# (Q16 ~ Q20 생략없이 완전히 유지)
qs_part2 = [
    {"qnum": 16, "title": "황금 문 톱니바퀴", "story": f"⚙️ <strong>[정비례 기어 링크]</strong><br><br>{poseidon}: \"이 산소 부족마저 통과하다니, 끈질긴 녀석들이군! 황금 문은 고정비 기어로 보호받는다. 출력 y가 구동각 x에 정비례하고 x=3일 때 y=15의 토크를 갖는다. x=5일 때는 어떨까?\"", "qtext": "<strong>Q16. [정비례 관계]</strong><br>y가 x에 정비례하고, x=3일 때 y=15이다. x=5일 때 y의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "기어 이가 맞물리지 않고 덜그럭거립니다!", "ans_check": "ans === '25'"},
    {"qnum": 17, "title": "황금 문 톱니바퀴", "story": f"⚙️ <strong>[거울 반사 조절 상수]</strong><br><br>{nereus}: \"메모리 장벽이 80% 열렸습니다! 기하학 광선 반사 경로 y = ax 식의 그래프가 거울 좌표 (2, -8)을 조준하도록 상수 a를 계산하십시오! 이제 곧 보물입니다!\"", "qtext": "<strong>Q17. [정비례 함수식]</strong><br>y = ax의 그래프가 점 (2, -8)을 지날 때, 상수 a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "거울 초점이 비틀어졌습니다! 다시 맞춰보세요.", "ans_check": "ans === '-4'"},
    {"qnum": 18, "title": "황금 문 톱니바퀴", "story": f"💎 <strong>[반비례 부력 링크]</strong><br><br>{nereus}: \"황금 문 너머의 보물이 보입니다! 부상하려면 부력 주머니 수 x개와 질량 y kg 사이의 반비례 관계를 연산하여 안전 균형을 맞춰야 합니다. 너무 무거우면 못 올라갑니다!\"", "qtext": "<strong>Q18. [반비례 관계 1]</strong><br>부력 장치 x개와 1개당 감당할 무게 y kg은 반비례한다. 4개를 달면 60kg을 감당할 때, 6개로 늘리면 몇 kg을 감당해야 하는가?", "placeholder": "숫자만 입력", "error": "부력 평형 균열 발생! 짐이 너무 무거워요.", "ans_check": "ans === '40'"},
    {"qnum": 19, "title": "황금 문 톱니바퀴", "story": f"💎 <strong>[인정과 명예로운 결말]</strong><br><br>{poseidon}: \"이럴 수가... 반비례와 정비례의 조화까지 완벽하게 이해하고 있다니! 너희는 단순한 도굴꾼이 아니었군. 반비례식 y = a/x를 완성시킬 최종 상수 a를 계산하라!\"", "qtext": "<strong>Q19. [반비례 관계 2]</strong><br>y가 x에 반비례하고 x=2일 때 y=10이다. y = a/x에서 a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "상수 불일치! 문이 꿈쩍도 안 합니다.", "ans_check": "ans === '20'"},
    {"qnum": 20, "title": "황금 문 톱니바퀴", "story": f"🔴 <strong>[최종 포탈 동기화]</strong><br><br>{nereus}: \"해냈습니다 {dyn_captain}!! 포세이돈이 우리 실력에 완전히 감탄했습니다! 마지막 탈출 포탈의 궤적 y = 12/x 가 점 (-3, k)를 통과하도록 최종 k값을 주입하십시오. 금화와 고대 지식을 챙겨서 해수면으로 부상합시다!!\"", "qtext": "<strong>Q20. [최종 암호 해독]</strong><br>반비례 그래프 y = 12/x 가 점 (-3, k)를 지난다. 최종 암호 k의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "차원 도약 포탈 동기화 실패! 조금만 더 집중하세요!", "ans_check": "ans === '-4'", "extra_class": "glitch-bg"}
]
qs.extend(qs_part2)

# Generate panels
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
        return "선택지에서 제4사분면을 골라주세요. x좌표가 양수(+)이고, y좌표가 음수(-)인 영역입니다."
    elif qnum == 7:
        return "선택지에서 제3사분면을 골라주세요. x좌표와 y좌표가 모두 음수(-)인 영역입니다."
    elif qnum == 8:
        return "곱이 음수(a × b < 0)라는 것은 두 수의 부호가 서로 다름을 뜻합니다. 뺀 값(a - b > 0)이 양수라는 것은 어느 쪽이 더 크다는 뜻일까요? 두 조건으로 a와 b의 부호를 판별해 보세요."
    elif qnum == 9:
        return "선택지에서 제3사분면을 골라주세요. P(a,b)가 2사분면이면 a<0, b>0 입니다. Q(a, -b)는 a<0, -b<0 이므로 둘 다 음수입니다."
    elif qnum == 10:
        return "점 P가 제3사분면 위의 점일 때 a와 b의 부호를 먼저 정해봅니다. 그 후 -a의 부호가 어떻게 바뀌는지 알아내어 점 Q의 (x좌표, y좌표) 부호를 분석해 보세요."
    elif qnum == 11:
        return "시간(x)은 계속 흘러가는데 이동한 거리(y)를 나타내는 그래프의 높이가 변하지 않고 평평합니다. 이는 잠수정이 어떤 상태임을 뜻할까요?"
    elif qnum == 12:
        return "일정한 속력으로 내려가므로 시간과 깊이는 정비례 관계입니다. 10분 동안 100m를 내려갔을 때, 절반의 시간인 5분 동안에는 몇 m를 내려갔을지 비례식을 세워 보세요."
    elif qnum == 13:
        return "선택지에서 '증가한다'를 골라주세요. 우상향하는 직선은 x축 값이 증가할 때 y축 값도 함께 올라갑니다."
    elif qnum == 14:
        return "수심 100m 지점에 5분 동안 계속 가만히 멈춰 있었다면, 멈춰 있는 동안 깊이(y값)가 변한 양은 얼마일지 생각해 보세요."
    elif qnum == 15:
        return "선택지에서 '우하향하는 모양'을 골라주세요. 시간이 흐름에 따라 남은 산소량이 점차 소모되어 줄어드므로 하향곡선을 그립니다."
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
    
    hint_btn_html = f'<button class="btn-hint" onclick="alert(\'💡 힌트: {q["hint"]}\')">💡 힌트</button>'
    qtext_hinted = qtext.replace('</strong>', f'</strong> {hint_btn_html}', 1)
    
    extra_class = q.get('extra_class', '')
    qbox_id = 'id="q10-main-box" style="display:none;"' if qnum == 10 else ''
    
    if "options" in q:
        options_html = ""
        for idx, opt in enumerate(q["options"]):
            options_html += f'''
                    <label class="radio-label" style="display: block; margin-bottom: 0.8rem; font-size: 1.1rem; cursor: pointer; text-align: left; padding: 0.5rem 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
                        <input type="radio" name="ans_group{qnum}" value="{opt}" style="margin-right: 0.8rem; transform: scale(1.2); cursor: pointer;"> {opt}
                    </label>'''
        input_html = f'''
                    <div class="options-group" id="ans{qnum}_group" style="margin-top: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem;">
                        {options_html}
                    </div>'''
    else:
        input_html = f'''
                    <div class="input-group">
                        <input type="text" id="ans{qnum}" placeholder="{placeholder}">
                    </div>'''

    panel = f'''
        <!-- Q{qnum} -->
        <div id="panel_q{qnum}" class="glass-panel {extra_class}">
            <h2>제 {qnum}구역: {title} <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/{img_map[qnum]}" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">{story}</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="question-box" {qbox_id}>
                <div class="question-content">
                    {qtext_hinted}
                    {input_html}
                </div>
            </div>
            <div class="error-msg" id="error{qnum}">{error}</div>
            <div class="btn-group">
                <button class="btn" onclick="checkQ{qnum}()">{'잠항 시작' if qnum==1 else '다음으로' if qnum < 20 else '탈출하기'}</button>
            </div>
        </div>
'''
    panels_html += panel

outro_html = f'''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>탈출 성공!</h1>
            <h2>아틀란티스의 보물</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/{img_map['outro']}" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">미션 결과를 연산 중입니다...</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
panels_html += outro_html

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
        gas_end_call = f'''
                // GAS 기록 종료 호출
                try {{
                    if (window.userRecordRow && typeof google !== 'undefined' && google.script && google.script.run) {{
                        google.script.run.recordEnd(window.userRecordRow, 'm1_04');
                    }}
                }} catch(e) {{
                    console.warn("구글 시트 종료 기록 실패:", e);
                }}
                
                // 멀티 엔딩 처리
                let outroDiv = document.getElementById("outro-dynamic-text");
                if (outroDiv) {{
                    let firstName = window.playerFirstName || "캡틴";
                    if (totalWrongCount < 5) {{
                        outroDiv.innerHTML = "패널에 숫자 '-4'를 입력하는 순간! 지잉- 하는 거대한 소리와 함께 고대 AI 포세이돈-V가 문을 활짝 열어줍니다.<br><br>{poseidon}: '훌륭하다. 수천 년 만에 아틀란티스의 지혜를 물려줄 진정한 후계자를 만났군.'<br><br>{nereus}: '" + firstName + " 캡틴! 완벽합니다! 금화와 지식이 쏟아집니다, 어서 챙겨서 부상합시다!'<br><br>여러분은 완벽한 수학적 통찰력으로 심해의 전설을 정복했습니다. <b>[칭호 획득: 심연의 좌표 마스터]</b> 미션 대성공!";
                    }} else {{
                        outroDiv.innerHTML = "패널에 숫자 '-4'를 입력하는 순간! 지잉- 하는 거친 마찰음과 함께 문이 간신히 열립니다.<br><br>{poseidon}: '오답이 너무 많지만... 끈기 하나는 인정해주마. 얼른 가져가라.'<br><br>{nereus}: '" + firstName + " 캡틴! 간신히 황금 문이 열렸습니다! 보물을 다 챙길 시간은 없습니다. 당장 부력 장치를 가동해야 합니다!'<br><br>여러분은 황급히 금화 몇 닢을 챙기고 해수면으로 솟구쳐 오릅니다. 상처투성이의 탈출이었지만 미션 성공!";
                    }}
                }}'''

    if "options" in q:
        get_ans_js = f'''
            const checkedOpt = document.querySelector('input[name="ans_group{qnum}"]:checked');
            const ans = checkedOpt ? checkedOpt.value : "";
        '''
    else:
        get_ans_js = f'''
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace('(','').replace(')','');
        '''

    reset_target_q = next((item for item in qs if item["qnum"] == reset_qnum), None)
    if reset_target_q and "options" in reset_target_q:
        reset_js = f'''
                    document.querySelectorAll('input[name="ans_group{reset_qnum}"]').forEach(el => el.checked = false);
        '''
    else:
        reset_js = f'''
                    document.getElementById('ans{reset_qnum}').value = '';
        '''

    js = f'''
        // Q{qnum}
        function checkQ{qnum}() {{
            {get_ans_js}
            if ({ans_check}) {{
                wrongCount = 0;
                {victory_call} {gas_end_call}
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
            }} else {{
                wrongCount++;
                totalWrongCount++;
                timeLeft -= 60;
                if (timeLeft < 0) timeLeft = 0;
                updateTimerDisplay();
                triggerTimerWarning();
                if (wrongCount >= 3) {{
                    showGlitchOverlay();
                    alert("🚨 3회 오답 패널티! {zone_name} 처음으로 이동됩니다.");
                    wrongCount = 0;
                    {reset_js}
                    nextStage('panel_q{qnum}', 'panel_q{reset_qnum}', {reset_prog});
                }} else {{
                    showError('panel_q{qnum}', 'error{qnum}', wrongCount);
                }}
            }}
        }}
'''
    js_checks += js

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
.timer-warning {
    animation: blink-red 0.2s 5;
    font-size: 1.5rem !important;
}
@keyframes blink-red {
    0%, 100% { color: #ef4444; text-shadow: 0 0 15px #ef4444; }
    50% { color: #ffffff; text-shadow: none; }
}
.glitch-overlay-screen {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(239, 68, 68, 0.15);
    z-index: 99999;
    display: none;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    pointer-events: none;
    box-sizing: border-box;
    border: 10px solid #ef4444;
    animation: pulse-border 0.2s infinite;
}
.glitch-overlay-text {
    font-family: 'Share Tech Mono', monospace;
    font-size: 3rem;
    color: #ef4444;
    font-weight: bold;
    text-shadow: 0 0 20px #ef4444;
    animation: shake 0.1s infinite;
}
.glitch-overlay-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.5rem;
    color: #ffffff;
    margin-top: 1rem;
}
@keyframes pulse-border {
    0%, 100% { border-color: #ef4444; background: rgba(239, 68, 68, 0.15); }
    50% { border-color: #ffffff; background: rgba(239, 68, 68, 0.3); }
}
.typing-cursor {
    animation: cursor-blink 0.8s infinite;
    font-weight: bold;
    color: var(--accent);
    margin-left: 2px;
}
@keyframes cursor-blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}
.radio-msg {
    color: #60a5fa;
    font-size: 0.95rem;
    margin-top: 0.5rem;
    font-weight: bold;
    text-shadow: 0 0 5px #3b82f6;
    text-align: center;
    animation: blink 1.5s infinite;
}
</style>
'''

glitch_html_js = '''
<!-- V3.0 UI Additions -->
<div id="glitchOverlay" class="glitch-overlay-screen">
    <div class="glitch-overlay-text">🚨 SYSTEM EXPLOITED 🚨</div>
    <div class="glitch-overlay-sub">ACCESS DENIED - CODE ERROR</div>
</div>

<!-- Game Over Panel -->
<div id="gameover" class="glass-panel">
    <h1 style="color: #ef4444; text-shadow: 0 0 15px #ef4444;">미션 실패 (GAME OVER)</h1>
    <h2>산소 고갈!</h2>
    <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/outro.png" alt="Game Over" class="panel-image" style="filter: grayscale(1) sepia(1) hue-rotate(-50deg);">
    <div class="story-box">
        <div class="story-text" style="color: #ef4444;">
            [포세이돈-V]: "시간 초과다! 역시 이 아틀란티스의 지혜를 받아들일 준비가 안 되어 있군. 돌아가라!"<br><br>
            잠수정의 산소 공급 장치가 완전히 멈췄습니다. 아쉽게도 탈출 좌표를 연산하지 못해 모험은 여기까지입니다. 숨을 고르고 다시 도전하세요!
        </div>
    </div>
    <button class="btn" style="margin-top: 2rem; background: #ef4444; border-color: #ef4444;" onclick="location.reload()">처음부터 다시 시도하기</button>
</div>

<script>
function showGlitchOverlay() {
    const overlay = document.getElementById('glitchOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
        setTimeout(() => overlay.style.display = 'none', 1500);
    }
}

// showError 함수 오버라이딩 (네레우스 오답 무전 대응)
function showError(panelId, errorId, wrongCount) {
    try { playError(); } catch(e) {} 
    triggerLockdownAlert();
    const panel = document.getElementById(panelId);
    const errMsg = document.getElementById(errorId);
    
    panel.classList.remove('shake');
    void panel.offsetWidth; 
    panel.classList.add('shake');
    
    errMsg.style.display = 'block';
    
    let radioDiv = panel.querySelector('.radio-msg');
    if (!radioDiv) {
        radioDiv = document.createElement('div');
        radioDiv.className = 'radio-msg';
        errMsg.parentNode.insertBefore(radioDiv, errMsg.nextSibling);
    }
    
    let firstName = window.playerFirstName || "캡틴";
    
    if (wrongCount === 1) {
        radioDiv.innerHTML = "📡 [네레우스]: '" + firstName + " 캡틴, 사소한 계산 실수일 겁니다. 다시 계산해주십시오!'";
    } else if (wrongCount === 2) {
        radioDiv.innerHTML = "📡 [네레우스]: '경고! 다음 오답은 페널티가 발생합니다! 신중하게 골라주세요!'";
    } else {
        radioDiv.innerHTML = "";
    }
    
    setTimeout(() => { 
        errMsg.style.display = 'none'; 
        if (radioDiv) radioDiv.innerHTML = "";
    }, 3500);
}
</script>
'''

timer_replacement = '''
        function startTimer() {
            if (timerId) return;
            updateTimerDisplay();
            timerId = setInterval(() => {
                timeLeft--;
                if (timeLeft <= 0) {
                    clearInterval(timerId);
                    updateTimerDisplay();
                    document.querySelectorAll('.glass-panel').forEach(p => p.classList.remove('active'));
                    const goPanel = document.getElementById('gameover');
                    if (goPanel) goPanel.classList.add('active');
                    else {
                        alert("⏰ 제한 시간 초과!");
                        location.reload();
                    }
                } else {
                    updateTimerDisplay();
                }
            }, 1000);
        }
'''

def replace_between(text, start_str, end_str, replacement):
    start_idx = text.find(start_str)
    if start_idx == -1:
        print(f"Warning: Start marker '{start_str}' not found!")
        return text
    end_idx = text.find(end_str, start_idx + len(start_str))
    if end_idx == -1:
        print(f"Warning: End marker '{end_str}' not found after start marker!")
        return text
    return text[:start_idx] + replacement + text[end_idx:]

# 1. 패널 HTML 치환
new_content = replace_between(content, '<!-- Q1 -->', '<script>', '<!-- Q1 -->\n' + panels_html + '\n    </div>\n    ')

# 2. JS 치환 (오차 없는 완벽한 문자열 구분선 치환 적용)
start_marker = "// Q1"
end_marker = "window.onload = () => {"
# 들여쓰기 공백을 포함해 검색
end_idx_raw = new_content.find(end_marker)
if end_idx_raw != -1:
    start_search = end_idx_raw
    while start_search > 0 and new_content[start_search - 1] in [' ', '\t']:
        start_search -= 1
    end_marker_with_indent = new_content[start_search:end_idx_raw + len(end_marker)]
else:
    end_marker_with_indent = end_marker

# replacement 끝에 end_marker_with_indent 를 덧붙이지 않음 (원천적인 중복 정의 해결)
new_content = replace_between(new_content, start_marker, end_marker_with_indent, start_marker + '\n' + js_checks + '\n\n        ')

# 3. CSS 주입
if ".glitch-text" not in new_content:
    new_content = new_content.replace('</style>', glitch_css)

# 4. GameOver HTML 주입
if "glitchOverlay" not in new_content:
    new_content = new_content.replace('</body>', glitch_html_js + '\n</body>')

# 5. 타이머 교체
timer_pattern = r'function startTimer\(\) \{[\s\S]*?updateTimerDisplay\(\);\s*\}\s*,\s*1000\);\s*\}'
new_content = re.sub(timer_pattern, timer_replacement.strip(), new_content)

# 6. 동적 이름 치환 JS 주입 (tryStartGame) - 복성 예외 처리 로직 추가 (f-string이 아님에 유의)
name_injection_pattern = r'(const sid = document\.getElementById\(\'studentId\'\);[\s\S]*?const sname = document\.getElementById\(\'studentName\'\);[\s\S]*?return;\s*\})'
double_name_js = r'''\1

            // 이름 동적 개인화 처리 (복성 예외 처리 반영 및 전역 변수 바인딩)
            try {
                const doubleLastNames = ["제갈", "황보", "사공", "남궁", "서문", "독고", "선우"];
                let rawName = sname.value.trim();
                let firstName = rawName;
                if (rawName.length > 2) {
                    let prefix2 = rawName.substring(0, 2);
                    if (doubleLastNames.includes(prefix2)) {
                        firstName = rawName.substring(2);
                    } else {
                        firstName = rawName.substring(1);
                    }
                }
                window.playerFirstName = firstName;
                document.querySelectorAll(".dynamic-captain-name").forEach(el => {
                    let originalRole = el.getAttribute("data-original-role") || el.innerText;
                    if (!el.hasAttribute("data-original-role")) {
                        el.setAttribute("data-original-role", originalRole);
                    }
                    el.innerHTML = firstName + " " + originalRole;
                });
            } catch(e) { console.error("이름 파싱 에러:", e); }'''

if "window.playerFirstName" not in new_content:
    new_content = re.sub(name_injection_pattern, double_name_js, new_content)

# 7. 타이머 중복 중괄호 찌꺼기 완전 소거 (빌더 레벨 멱등성 보장 조치)
if "function nextStage" in new_content:
    timer_body_end = new_content.find("function startTimer() {")
    if timer_body_end != -1:
        normal_end = new_content.find("}, 1000);\n        }", timer_body_end)
        if normal_end != -1:
            normal_end_pos = normal_end + len("}, 1000);\n        }")
            next_stage_pos = new_content.find("function nextStage", normal_end_pos)
            if next_stage_pos != -1:
                new_content = new_content[:normal_end_pos] + "\n\n        " + new_content[next_stage_pos:]

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated successfully.")
