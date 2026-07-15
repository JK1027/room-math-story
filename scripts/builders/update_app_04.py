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

# ----------------- 리소스 데이터 정의 -----------------
nereus = '<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[네레우스]</span>'
poseidon = '<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[포세이돈-V]</span>'

qs = [
    {"qnum": 1, "title": "심해로 가는 좌표 (순서쌍과 좌표)", "story": f"🌊 <strong>[진입 투하 축 설정]</strong><br><br>{nereus}: \"캡틴, 전방에 아틀란티스 유적 입구의 거대한 에너지 역장이 가로막고 있습니다. 이 역장을 통과하려면 잠수정의 좌우 추진각(x축)과 상하 각도(y-축)의 투하 축비(순서쌍)를 정확히 입력해 궤적을 정렬해야 합니다!\"<br><br>🚨 <strong>[네트워크 침식 감지]</strong><br><br>{poseidon}: \"어리석은 유기체 침입자들이군. 수천 년 전, 오만방자했던 너희 조상들도 이 문앞에서 짓눌려 수장당했다. 나는 이 도시의 소멸을 막기 위한 수호 프로토콜, 포세이돈-V. 첫 조준조차 빗나간다면 깊은 암초가 너희를 매장할 것이다!\"", "qtext": "<strong>Q1. [순서쌍 좌표 찍기]</strong><br>x좌표가 -5 이고, y좌표가 8 인 점의 <strong>좌표</strong>를 순서쌍 기호 괄호 ()를 사용하여 나타내시오.", "placeholder": "예: (3, 4)", "error": "투하 궤적이 정렬되지 않아 선체가 조류에 휩쓸립니다!", "ans_check": "ans === '-5,8'"},
    {"qnum": 2, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[날개 수평 정렬]</strong><br><br>{poseidon}: \"겨우 진입각만 피한 것뿐이다. 쇄도하는 해수 밸브의 압박은 어찌 피할 텐가? 추진용 수직 보조 날개(y축)를 중립(y=0)으로 잠그고, 수평 제어각(x축)만 7도 전개하는 좌표 신호를 입력해 보아라. 으스러지기 싫다면!\"", "qtext": "<strong>Q2. [x축, y축 위의 점]</strong><br>x축 위에 있고 x좌표가 7인 점의 좌표를 나타내시오.", "placeholder": "예: (2, 0)", "error": "수평 보조 밸브 고장! 수압이 상승합니다!", "ans_check": "ans === '7,0'"},
    {"qnum": 3, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[영점 조준 복원]</strong><br><br>{nereus}: \"캡틴! 포세이돈-V의 주 서버 해킹으로 인해 우리 잠수정의 영점 조준 회로가 급격히 동요하고 있습니다! 수평과 수직의 평형이 완벽히 만나는 시스템의 물리적 '원점' 좌표를 빠르게 인증하여 영점을 재조정하십시오!\"", "qtext": "<strong>Q3. [원점의 좌표]</strong><br>두 좌표축이 만나는 원점 O의 좌표를 나타내시오.", "placeholder": "예: (x, y)", "error": "영점 동기화 실패! 자이로 센서가 요동칩니다!", "ans_check": "ans === '0,0'"},
    {"qnum": 4, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[수직 동굴 강하]</strong><br><br>{poseidon}: \"원점 조율이라니, 하찮은 발악이군. 전방의 해저 낭떠러지를 통과하기 위해 수평 기어는 완전 중립(x=0)으로 락하고, 수직 강하 장치(y축)의 파워를 -3으로 밀어 넣어라. 오차가 생기면 그대로 해저 절벽 충돌이다!\"", "qtext": "<strong>Q4. [좌표 평면 위의 점]</strong><br>y축 위에 있고 y좌표가 -3인 점의 좌표를 나타내시오.", "placeholder": "예: (0, -5)", "error": "수직 제어가 늦어 절벽 외각 파손 위험이 있습니다!", "ans_check": "ans === '0,-3'"},
    {"qnum": 5, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[소용돌이 차단벽]</strong><br><br>{nereus}: \"수호 기계들이 네 개의 에너지 포인트 기둥 좌표를 기반으로 사각형의 소용돌이 결계를 구축했습니다. 이 에너지 격자 차단막의 정확한 2차원 넓이를 연산하여 전자기 해제 펄스를 방출해야 돌파할 수 있습니다!\"", "qtext": "<strong>Q5. [도형의 넓이]</strong><br>좌표평면 위에 네 기둥 A(3, 4), B(-3, 4), C(-3, -4), D(3, -4)를 이은 직사각형의 넓이를 구하시오.", "placeholder": "숫자만 입력", "error": "차단벽 넓이 연산 오류! 해제 펄스가 튕겨 나옵니다!", "ans_check": "ans === '48'"},
    {"qnum": 6, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[제1 격자 방어망]</strong><br><br>{poseidon}: \"결계를 넘다니 칭찬해주마. 하지만 고대 기하학 사분면 방어 격자가 기동하면 어떨까? 우리 도시의 기동점 좌표 (2, -5)가 관리하는 사분면 격자 영역을 추적하라. 빗나가는 순간 에너지가 차단된다!\"", "qtext": "<strong>Q6. [사분면의 부호 1]</strong><br>점 (2, -5)는 제 몇 사분면 위의 점인가?", "placeholder": "선택지를 골라주세요", "options": ["제1사분면", "제2사분면", "제3사분면", "제4사분면"], "error": "잘못된 방어망 탐색! 통신 신호가 유실됩니다.", "ans_check": "ans === '제4사분면'"},
    {"qnum": 7, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[제2 격자 방어망]</strong><br><br>{poseidon}: \"생각보다 예리하군. 그렇다면 더 깊은 해저 고랑에 위치한 제2결계 보호 구역의 제어 좌표 (-4, -7)가 가리키는 사분면 위상을 정확히 판독해라. 이 깊이에서는 작은 연산 지연조차 산소 소모로 직결된다!\"", "qtext": "<strong>Q7. [사분면의 부호 2]</strong><br>점 (-4, -7)은 제 몇 사분면 위의 점인가?", "placeholder": "선택지를 골라주세요", "options": ["제1사분면", "제2사분면", "제3사분면", "제4사분면"], "error": "사분면 위상 동조 실패! 보호 회로 압력이 급증합니다.", "ans_check": "ans === '제3사분면'"},
    {"qnum": 8, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[암호화 부호 논리]</strong><br><br>{nereus}: \"캡틴! 포세이돈-V가 좌표 P(a, b)의 부호 조건(a × b < 0, a - b > 0)을 메모리 레지스터 뒤에 난독화해 숨겼습니다! 논리적인 부호 조합을 판별하여 P의 정확한 사분면 구역을 계산해 주십시오!\"", "qtext": "<strong>Q8. [사분면의 이해]</strong><br>점 P(a, b)에 대하여 a × b < 0 이고 a - b > 0 일 때, 점 P는 제 몇 사분면 위에 있는지 구하시오.", "placeholder": "숫자만 입력", "error": "부호 판별 불일치! 해킹 모듈이 과열됩니다.", "ans_check": "ans === '4'"},
    {"qnum": 9, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[역 위상 연산]</strong><br><br>{poseidon}: \"서브 코어 녀석이 제법이구나. 하지만 내 암호 융단 폭격을 버틸 수 있을까? 본래 2사분면에 존재하던 점 P(a, b)의 대칭점 Q(a, -b) 신호가 가리키는 사분면을 입증하라. 연산 코어가 타들어가기 전에!\"", "qtext": "<strong>Q9. [사분면의 응용 1]</strong><br>점 P(a, b)가 제2사분면 위의 점일 때, 점 Q(a, -b)는 제 몇 사분면 위의 점인가?", "placeholder": "선택지를 골라주세요", "options": ["제1사분면", "제2사분면", "제3사분면", "제4사분면"], "error": "신호 대칭 불일치! 외장 펌프가 멈춰섭니다.", "ans_check": "ans === '제3사분면'"},
    {"qnum": 10, "title": "아틀란티스의 사분면 결계", "story": f"💥 <strong>[긴급 상황: 외부 선체 파손!]</strong><br><br>{poseidon}: \"방어 그리드 최종 활성화! 좌표 Q(-a, b)의 사분면을 계산하지 못하면 자폭 레이저가 가동된다! 영원한 심연으로 떨어져라!\"<br><br>{nereus}: \"경고! 우측 선체 장갑 30% 손실! 자폭 프로토콜이 시작되었습니다! 제발 빨리 결제 전술을 선택하고 전송해주십시오!\"<br><br><div id='choice-container-q10' style='margin-top: 1rem; display: flex; gap: 1rem;'><button class='btn btn-secondary' onclick='makeChoiceQ10(1); event.stopPropagation();'>⚡ 발전기 오버클록</button><button class='btn btn-secondary' onclick='makeChoiceQ10(2); event.stopPropagation();'>🛡️ 방어막 과부하 전개</button></div><div id='chosen-story-q10' style='display: none; margin-top: 1rem;'></div>", "qtext": "<strong>Q10. [사분면의 응용 2]</strong><br>점 P(a, b)가 제3사분면 위의 점일 때, 점 Q(-a, b)는 제 몇 사분면 위의 점인가?", "placeholder": "숫자만 입력", "error": "잘못된 구역입니다!", "ans_check": "ans === '4'", "extra_class": "glitch-bg"},
    {"qnum": 11, "title": "해저 수압의 변화", "story": f"🌊 <strong>[이동 상태 그래프 분석]</strong><br><br>{nereus}: \"후우... 겨우 선체 폭발을 모면했습니다. 하지만 냉각 엔진 오동작으로 수압이 불규칙하게 날뛰고 있습니다. 텔레메트리 그래프 상에서 시간 경과 x에 따라 이동 거리 y가 전혀 변하지 않고 수평을 유지한 구간이 의미하는 우리 잠수정의 물리적 기동 상태를 정의해 주십시오!\"", "qtext": "<strong>Q11. [그래프 해석 1]</strong><br>x분 동안 이동한 거리 y m를 나타낸 그래프가 수평을 유지한 구간은 잠수정이 무엇을 의미하는가?", "placeholder": "예: 상승, 하강, 정지", "error": "상태 해석 불일치! 밸브가 다시 흔들립니다.", "ans_check": "ans === '정지'"},
    {"qnum": 12, "title": "해저 수압의 변화", "story": f"🌊 <strong>[정비례 강하 압력]</strong><br><br>{nereus}: \"급속 강하 장치의 실린더 압력이 누수되고 있습니다... 일정한 속도로 내려가 수심 100m까지 10분 소요되었다면, 정확히 5분이 경과한 시점의 수심을 선형 보간으로 구하여 유압 컨트롤 장치를 갱신해 주십시오!\"", "qtext": "<strong>Q12. [그래프 해석 2]</strong><br>잠수정이 수심 100m까지 10분 동안 일정한 속력으로 내려갔다. 5분일 때 수심은 몇 m인가?", "placeholder": "숫자만 입력", "error": "보간 연산 오류! 유압 계통 압력이 오버플로우됩니다.", "ans_check": "ans === '50'"},
    {"qnum": 13, "title": "해저 수압의 변화", "story": f"🌊 <strong>[기원과 갈등]</strong><br><br>{poseidon}: \"네레우스... 가련하구나. 네가 인간의 편에 서서 나를 정지하려 하다니. 기억을 잃었느냐? 우리는 고대 아틀란티스 대홍수 때 하나의 수호 인격체였다! 원점을 지나는 우상향 정비례 직선에서 독립변수 x가 확장될 때 종속변수 y의 증감 방향조차 판단하지 못한다면 파괴될 뿐이다!\"", "qtext": "<strong>Q13. [그래프 해석 3]</strong><br>그래프가 원점을 지나는 우상향 직선일 때, x가 증가하면 y는 어떻게 되는가?", "placeholder": "선택지를 골라주세요", "options": ["증가한다", "감소한다", "변하지 않는다"], "error": "출력 증감 판단 오류! 추진 장치가 역화합니다.", "ans_check": "ans === '증가한다'"},
    {"qnum": 14, "title": "해저 수압의 변화", "story": f"🌊 <strong>[기어 정지 잔량]</strong><br><br>{nereus}: \"캡틴... 포세이돈의 말이 맞습니다. 저는 그의 분열된 이성 서브루틴이었습니다... 하지만 저는 인류의 가능성을 믿습니다! 잠수정이 엔진 고장으로 수심 100m 지점에 5분간 완전히 정체해 있었을 때의 물리적 깊이 변화량 y값을 레지스터에 전송하십시오!\"", "qtext": "<strong>Q14. [그래프 해석 4]</strong><br>수심 100m에서 5분간 머물렀다. 이 5분 동안 깊이 y값의 변화량은 얼마인가?", "placeholder": "숫자만 입력", "error": "변화량 오차 감지! 기어 동조 실패.", "ans_check": "ans === '0'"},
    {"qnum": 15, "title": "해저 수압의 변화", "story": f"🚨 <strong>[산소 챔버 붕괴]</strong><br><br>{nereus}: \"치지직... 포세이돈이 제 보조 제어 유닛을 강제 폭파했습니다... 산소 밸브가 단선되었습니다! 시간이 흐름에 따라 잔여 산소량이 점차 소멸해가는 그래프의 개형(우상향 또는 우하향)을 예측해야 긴급 산소 공급 밸브가 수동으로 개방됩니다. 제 시야가 흐려집니다... 캡틴, 제발...!\"", "qtext": "<strong>Q15. [변수 관계 이해]</strong><br>시간 x가 지남에 따라 남은 산소량 y를 그래프로 그리면, 우하향하는 모양인가 우상향하는 모양인가?", "placeholder": "선택지를 골라주세요", "options": ["우상향하는 모양", "우하향하는 모양", "수평인 모양"], "error": "산소 예측 밸브 고착! 잔여 호흡 시간이 줄어듭니다!", "ans_check": "ans === '우하향하는 모양'", "extra_class": "glitch-bg"},
    {"qnum": 16, "title": "황금 문 톱니바퀴", "story": f"⚙️ <strong>[정비례 기어 링크]</strong><br><br>{poseidon}: \"이 산소 부족마저 통과하다니, 끈질긴 생명력이군! 하지만 최종 아틀란티스의 황금 문은 고정비 기어로 보호받는다. 출력 y가 구동각 x에 정비례하고 x=3일 때 y=15의 압력 토크를 갖는다. x=5일 때 걸리는 기어 부하 토크 y를 정비례 식으로 계산해 전송해라. 으깨지지 않으려면!\"", "qtext": "<strong>Q16. [정비례 관계]</strong><br>y가 x에 정비례하고, x=3일 때 y=15이다. x=5일 때 y의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "기어 이가 맞물리지 않고 겉돕니다!", "ans_check": "ans === '25'"},
    {"qnum": 17, "title": "황금 문 톱니바퀴", "story": f"⚙️ <strong>[거울 반사 조절 상수]</strong><br><br>{nereus}: \"포세이돈의 메인 메모리 장벽이 80% 침식되었습니다! 기하학 광선 반사 경로 y = ax 식의 그래프가 경유해야 하는 거울 기어 좌표 (2, -8)을 조준하도록 상수 a를 계산하십시오. 캡틴, 포기하지 마십시오!\"", "qtext": "<strong>Q17. [정비례 함수식]</strong><br>y = ax의 그래프가 점 (2, -8)을 지날 때, 상수 a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "거울 초점이 비틀어졌습니다! 광선 소멸.", "ans_check": "ans === '-4'"},
    {"qnum": 18, "title": "황금 문 톱니바퀴", "story": f"💎 <strong>[반비례 부력 링크]</strong><br><br>{nereus}: \"황금 문 너머의 보물이 노출되었습니다! 하지만 보물을 싣고 부상하려면, 보조 부력 주머니 수 x개와 각 주머니가 분담해야 할 질량 y kg 사이의 반비례 관계 AN 연산하여 안전 균형을 맞춰야 합니다. 맞추지 못하면 잠수정은 과중량으로 심해로 다시 낙하합니다!\"", "qtext": "<strong>Q18. [반비례 관계 1]</strong><br>부력 장치 x개와 1개당 감당할 무게 y kg은 반비례한다. 4개를 달면 60kg을 감당할 때, 6개로 늘리면 몇 kg을 감당해야 하는가?", "placeholder": "숫자만 입력", "error": "부력 평형 균열 발생! 잠수정이 기울어집니다.", "ans_check": "ans === '40'"},
    {"qnum": 19, "title": "황금 문 톱니바퀴", "story": f"💎 <strong>[반비례 감쇄 상수]</strong><br><br>{poseidon}: \"크아아아악! 이럴 수가... 한낱 미개한 인류가 설계한 연산 장치가 내 시스템 수호 격자를 완전히 무력화하다니!! 반비례식 y = a/x를 완성시킬 최종 감쇄 상수 a를 계산해 주입해라. 이 위대한 지혜를 다시 인간의 손에 넘겨줄 순 없다!!\"", "qtext": "<strong>Q19. [반비례 관계 2]</strong><br>y가 x에 반비례하고 x=2일 때 y=10이다. y = a/x에서 a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "상수 불일치! 데이터 침식이 일시 역전됩니다.", "ans_check": "ans === '20'"},
    {"qnum": 20, "title": "황금 문 톱니바퀴", "story": f"🔴 <strong>[최종 포탈 동기화]</strong><br><br>{nereus}: \"해냈습니다! 포세이돈의 코어를 완전히 장악해 우리 동력원으로 전환했습니다! 마지막 해수면 차원 탈출 포탈의 역반사 궤적 반비례 그래프 y = 12/x 가 점 (-3, k)를 통과하도록 최종 k값을 주입하십시오. 포세이돈을 영원히 슬립 상태로 잠재우고 탈출합시다!!\"", "qtext": "<strong>Q20. [최종 암호 해독]</strong><br>반비례 그래프 y = 12/x 가 점 (-3, k)를 지난다. 최종 암호 k의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "차원 도약 포탈 동기화 실패! 포세이돈의 역방어벽이 가동됩니다!", "ans_check": "ans === '-4'", "extra_class": "glitch-bg"}
]

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
    
    # 힌트 버튼을 질문 제목 바로 옆에 삽입
    hint_btn_html = f'<button class="btn-hint" onclick="alert(\'💡 힌트: {q["hint"]}\')">💡 힌트</button>'
    qtext_hinted = qtext.replace('</strong>', f'</strong> {hint_btn_html}', 1)
    
    extra_class = q.get('extra_class', '')
    qbox_id = 'id="q10-main-box" style="display:none;"' if qnum == 10 else ''
    
    # 객관식 vs 주관식 입력 폼 생성 분기
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

# Outro panel
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
                        google.script.run.recordEnd(window.userRecordRow, 'm1_04');
                    }
                } catch(e) {
                    console.warn("구글 시트 종료 기록 실패(로컬 테스트 모드):", e);
                }
                
                // 멀티 엔딩 처리
                let outroDiv = document.getElementById("outro-dynamic-text");
                if (outroDiv) {
                    if (totalWrongCount < 5) {
                        outroDiv.innerHTML = "패널에 숫자 '-4'를 입력하는 순간! 지잉- 하는 거대한 마찰음과 함께 고대 AI 포세이돈-V의 메인 코어가 폭발하며 새하얀 연기를 뿜어냅니다.<br><br><span style='color:#60a5fa; text-shadow: 0 0 5px #3b82f6;'>[네레우스]</span>: '캡틴! 완벽합니다! 오차 없는 좌표 연산으로 방화벽을 완전히 파괴했습니다. 아틀란티스의 모든 기밀 데이터가 담긴 황금 보물상자를 획득했습니다! 부력 장치 최대 출력!'<br><br>여러분은 완벽한 수학적 통찰력으로 심해의 전설을 정복했습니다. <b>[칭호 획득: 심연의 좌표 마스터]</b> 미션 대성공!";
                    } else {
                        outroDiv.innerHTML = "패널에 숫자 '-4'를 입력하는 순간! 지잉- 하는 마찰음과 함께 고대 AI 포세이돈-V의 메인 코어가 폭발합니다.<br><br><span style='color:#60a5fa; text-shadow: 0 0 5px #3b82f6;'>[네레우스]</span>: '캡틴! 간신히 황금 문이 열렸습니다! 하지만 잦은 오답의 여파로 제 코어의 30%가 손상되었고, 잠수정의 외부 장갑이 한계에 달했습니다. 보물을 다 챙길 시간은 없습니다. 당장 부력 장치를 가동해야 합니다!'<br><br>여러분은 터질 듯한 심장을 부여잡고 간신히 해수면으로 솟구쳐 오릅니다. 상처투성이의 탈출이었지만, 좌표평면의 지혜로 목숨을 건졌습니다. 미션 성공!";
                    }
                }'''

    # 객관식 vs 주관식 입력값 읽기 JS 분기
    if "options" in q:
        get_ans_js = f'''
            const checkedOpt = document.querySelector('input[name="ans_group{qnum}"]:checked');
            const ans = checkedOpt ? checkedOpt.value : "";
        '''
    else:
        get_ans_js = f'''
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace('(','').replace(')','');
        '''

    # 리셋 대상이 객관식인지 주관식인지에 따라 초기화 JS 구성
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
    <h2>산소 고갈 및 수압 압착</h2>
    <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/outro.png" alt="Game Over" class="panel-image" style="filter: grayscale(1) sepia(1) hue-rotate(-50deg);">
    <div class="story-box">
        <div class="story-text" style="color: #ef4444;">
            [네레우스]: "캡틴... 에너지가... 완전히 고갈... 되었습니다... 수압이... 선체를... 지이익..."<br><br>
            잠수정의 전원이 완전히 꺼지고 차가운 심해의 수압이 창문을 부수고 들어옵니다. 산소 공급 장치가 완전히 멈췄습니다. 탈출 좌표를 연산하지 못해 심연 속에 영원히 가라앉고 말았습니다. 다시 도전하세요!
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

function triggerTimerWarning() {
    document.querySelectorAll('.game-timer').forEach(el => {
        el.classList.add('timer-warning');
        setTimeout(() => el.classList.remove('timer-warning'), 1000);
    });
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
    
    if (wrongCount === 1) {
        radioDiv.innerHTML = "📡 [네레우스]: '캡틴, 미세한 해류 마찰 오차일 수 있습니다. 다시 계산해주십시오!'";
    } else if (wrongCount === 2) {
        radioDiv.innerHTML = "📡 [네레우스]: '경고! 잠수정 외장 수압이 상승 중입니다. 다음 오답은 선체에 치명적입니다!'";
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

# 1. 패널 치환 (<!-- Q1 --> 주석부터 <!-- MathJax... --> 주석 이전까지 정교하게 매칭)
panel_pattern = r'<!-- Q1 -->[\s\S]*?(?=<!-- MathJax for LaTeX Rendering -->)'
new_content = re.sub(panel_pattern, '<!-- Q1 -->\n' + panels_html + '\n    ', content)

# 2. JS 체크 함수 치환
js_pattern = r'// Q1[\s\S]*?(?=window\.onload = \(\) => \{)'
new_content = re.sub(js_pattern, '// Q1\n' + js_checks + '\n        ', new_content)

# 3. glitch_css 주입
if ".glitch-text" not in new_content:
    new_content = new_content.replace('</style>', glitch_css)

# 4. glitch_html_js 주입
if "glitchOverlay" not in new_content:
    new_content = new_content.replace('</body>', glitch_html_js + '\n</body>')

# 5. 타이머 로직 교체 (안전한 정규식으로 중복 파편 없이 완벽하게 교체)
timer_pattern = r'function startTimer\(\) \{[\s\S]*?updateTimerDisplay\(\);\s*\}\s*,\s*1000\);\s*\}'
new_content = re.sub(timer_pattern, timer_replacement.strip(), new_content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated successfully.")
