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
clio = "<span style='color: #c084fc; text-shadow: 0 0 5px #a855f7;'>[클리오]</span>"
poseidon = "<span class='glitch-text' style='color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;'>[포세이돈-V]</span>"
trident = "<span class='glitch-text' style='color: #fb923c; font-weight: bold; text-shadow: 0 0 5px #f97316;'>[트라이던트]</span>"
dyn_captain = "<span class='dynamic-captain-name'>캡틴</span>"

qs = [
    {"qnum": 1, "options": ["-5,8", "-5,8 아님", "알 수 없음", "해 없음"], "title": "심해로 가는 좌표 (순서쌍과 좌표)", "story": f"🌊 <strong>[진입 투하 축 설정]</strong><br><br>쿵! 하는 둔탁한 소리와 함께 크로노스 호의 선미가 해저 암벽에 스친다. 경고등이 요란하게 깜빡이고, 수압 게이지 바늘이 위험 대역으로 조금씩 전진한다.<br><br>{nereus}: \"조류가 너무 거세서 자동 방향 지시계가 먹통이 되었습니다! 수문장 AI가 요구하는 진입각 순서쌍 좌표를 정렬해야 해요! {dyn_captain}, 어서 이 좁은 격벽 틈새로 진입할 수 있는 순서쌍 부호를 주입해 주세요! 안 그러면 선체가 조류에 휩쓸려 벽에 충돌합니다!\"<br><br>{poseidon}: \"하찮은 지능의 척도로 감히 첫 관문을 뚫으려 드는가. 수평과 수직의 엄격한 기약(순서쌍)을 제출하라! 수학의 가장 기초조차 파악하지 못하는 어리석은 자들은 이 어두운 심연에서 영원히 길을 잃을 것이다!\"", "qtext": "<strong>Q1. [순서쌍 좌표 찍기]</strong><br>x좌표가 -5 이고, y좌표가 8 인 점의 <strong>좌표</strong>를 순서쌍 기호 괄호 ()를 사용하여 나타내시오.", "placeholder": "예: (3, 4)", "error": "투하 궤적이 정렬되지 않아 선체가 조류에 흔들립니다!", "ans_check": "ans === '-5,8'"},
    {"qnum": 2, "options": ["7,0", "7,0 아님", "알 수 없음", "해 없음"], "title": "심해로 가는 좌표", "story": f"🌊 <strong>[날개 수평 정렬]</strong><br><br><i>조사관이 키패드에 (-5, 8)을 정확히 주입하는 순간, 선체 좌측의 수력 추진기 보조 밸브가 강력한 증기를 내뿜으며 크로노스 호를 90도 회전시킨다. 잠수정은 뾰족한 창날처럼 튀어나온 해저 바위들을 스치듯 빠져나와 좁고 긴 해저 협곡으로 빠르게 미끄러져 들어간다.</i><br><br>{clio}: \"나이스 샷, {dyn_captain}! 역시 내 밸브 개조가 빛을 발했네요. 그런데 앞쪽에 또 다른 좁아지는 해류 통로가 보입니다!\"<br><br>{nereus}: \"유속이 두 배로 빨라지고 있어요! 추진용 날개의 정밀한 정렬이 시급합니다!\"<br><br>{poseidon}: \"겨우 기어 진입각 하나 맞췄을 뿐이다. 몰아치는 급류의 이빨이 너희를 찢어발기기 전에, 추진용 수직 날개(y축)를 중립(y=0)으로 굳게 잠그고, 오직 수평(x축) 우측으로만 7도 전개하는 좌표 빗장 신호를 인젝션해 보아라!\"", "qtext": "<strong>Q2. [x축, y축 위의 점]</strong><br>x축 위에 있고 x좌표가 7인 점의 좌표를 나타내시오.", "placeholder": "예: (2, 0)", "error": "수평 보조 밸브 고장! 수압 경고등이 켜집니다!", "ans_check": "ans === '7,0'"},
    {"qnum": 3, "options": ["0,0", "0,0 아님", "알 수 없음", "해 없음"], "title": "심해로 가는 좌표", "story": f"🌊 <strong>[영점 조준 복원]</strong><br><br><i>추진 날개가 정확히 (7, 0)으로 정렬되자 잠수정은 협곡 바닥의 거센 급류를 타고 날렵하게 미끄러져 내려간다. 그러나 갑자기 사원의 기단에서 스파크를 일으키며 뿜어져 나온 푸른색 자력선들이 잠수정의 강철 하부를 관통한다. 삐-이이- 하는 이명과 함께 계기판의 모든 자이로 회로와 나침반이 제멋대로 돌기 시작한다.</i><br><br>{clio}: \"으아아! 자력 펄스 비상! 메인 제어 신호가 꼬여서 자이로 센서가 완전히 가버렸어요!\"<br><br>{nereus}: \"수평과 수직 좌표축이 만나는 가장 완벽한 대칭점인 '원점'의 기하학적 주소를 인증해 주세요! 이 센서의 영점을 다시 잡아야 제어력을 되찾을 수 있습니다!\"", "qtext": "<strong>Q3. [원점의 좌표]</strong><br>두 좌표축이 만나는 원점 O의 좌표를 나타내시오.", "placeholder": "예: (x, y)", "error": "영점 동기화 실패! 자이로 센서가 빙글빙글 돕니다!", "ans_check": "ans === '0,0'"},
    {"qnum": 4, "options": ["0,-3", "0,-3 아님", "알 수 없음", "해 없음"], "title": "심해로 가는 좌표", "story": f"🌊 <strong>[수직 동굴 강하]</strong><br><br><i>조사관이 영점 좌표 (0, 0)을 정확히 입력하자 계기판의 붉은 노이즈가 싹 사라지며 자이로 센서가 중심을 단단히 잡는다. 하지만 잠수정의 서치라이트 불빛이 닿은 전방에는 한 치 앞도 보이지 않는 수직 암흑 구멍이 끝없이 내려앉아 있다.</i><br><br>{poseidon}: \"원점을 다시 세워 기어코 중심을 잡는구나. 하지만 이 깊고 캄캄한 수직 동굴은 침입자의 무덤이다. 수평 날개(x)는 완벽한 중립(0)으로 고정하고, 오직 수직 하강 추진력(y)만을 아래 방향인 -3으로 정렬해 내려가라. 만약 속도나 방향을 잘못 잡는다면, 수천 톤의 암석 아래 찌그러진 강철 고철이 되리라.\"", "qtext": "<strong>Q4. [좌표 평면 위의 점]</strong><br>y축 위에 있고 y좌표가 -3인 점의 좌표를 나타내시오.", "placeholder": "예: (0, -5)", "error": "수직 제어가 늦어 절벽에 부딪힐 뻔했습니다!", "ans_check": "ans === '0,-3'"},
    {"qnum": 5, "options": ["46", "48", "50", "96"], "title": "심해로 가는 좌표", "story": f"🌊 <strong>[소용돌이 차단벽]</strong><br><br><i>잠수정이 좁은 수직 틈새를 부드럽게 통과하자, 마침내 넓고 신비로운 해저 지하 사원의 입구가 나타난다. 그러나 사원 입구 앞에는 고대 황금 에너지 기둥 네 개가 사각 구도로 배치되어 이글거리며 푸른빛의 소용돌이 장막을 내뿜어 앞길을 가로막는다.</i><br><br>{clio}: \"{dyn_captain}, 저 황금빛 결계 기둥 4개가 만드는 전기 장막의 면적을 구해야 펄스포 주파수를 동조시킬 수 있어요! 네레우스, 좌표 불러줘!\"<br><br>{nereus}: \"네! 기둥의 좌표는 A(3, 4), B(-3, 4), C(-3, -4), D(3, -4)입니다. 어서 이 직사각형 영역의 정확한 넓이를 구해 주세요!\"", "qtext": "<strong>Q5. [도형의 넓이]</strong><br>좌표평면 위에 네 기둥 A(3, 4), B(-3, 4), C(-3, -4), D(3, -4)를 이은 직사각형의 넓이를 구하시오.", "placeholder": "숫자만 입력", "error": "차단벽 넓이 연산 오류! 잠수정이 튕겨 나옵니다!", "ans_check": "ans === '48'"},
    {"qnum": 6, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[제1 격자 방어망]</strong><br><br><i>위이잉- 갑자기 조종석 전면 붉은 경보등이 점멸하며 뾰족하고 거친 금속성 디자인의 가디언 홀로그램이 포세이돈의 자리를 가로막고 나타난다.</i><br><br>{trident}: \"침입자 발견! 살상 모듈을 기동한다! 포세이돈 님, 왜 이 하찮은 벌레들과 대화를 나누십니까? 즉시 사분면 결계로 납작하게 부수겠습니다!\"<br><br>{poseidon}: \"트라이던트여, 기하학의 수치를 푸는 지혜를 시험하는 것이 먼저다. {dyn_captain}, 우리의 기동 좌표인 (2, -5)가 관장하는 사분면 격자를 정확히 지목하라!\"", "qtext": "<strong>Q6. [사분면의 부호 1]</strong><br>점 (2, -5)는 제 몇 사분면 위의 점인가?", "placeholder": "선택지를 골라주세요", "options": ["제1사분면", "제2사분면", "제3사분면", "제4사분면"], "error": "잘못된 방어망 탐색! 빙글빙글 돌아갑니다.", "ans_check": "ans === '제4사분면'"},
    {"qnum": 7, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[제2 격자 방어망]</strong><br><br><i>제4사분면 통로가 열리자 잠수정이 진입한다. 그러나 트라이던트가 거대한 밸브를 돌려 차가운 흙과 어두운 부유물을 살포한다.</i><br><br>{trident}: \"포세이돈 님의 아량을 바란 것인가? 두 번째 락인 좌표 (-4, -7)를 대라! 이 안개 속에서 헤매다 선체가 찌그러지는 꼴을 지켜보아라!\"", "qtext": "<strong>Q7. [사분면의 부호 2]</strong><br>점 (-4, -7)은 제 몇 사분면 위의 점인가?", "placeholder": "선택지를 골라주세요", "options": ["제1사분면", "제2사분면", "제3사분면", "제4사분면"], "error": "사분면 위상 동조 실패! 회로가 삐걱거립니다.", "ans_check": "ans === '제3사분면'"},
    {"qnum": 8, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[암호화 부호 논리]</strong><br><br><i>안개가 걷히자 청동 톱니바퀴 여러 개가 벽면에 박혀 돌아가고 있다.</i><br><br>{clio}: \"저 톱니바퀴 빗장을 풀어야 해요! 네레우스, 기호 좀 판독해 봐!\"<br><br>{nereus}: \"a × b < 0 이고 a - b > 0 이라는 수치를 만족하는 점 P의 사분면 번호를 찾아야 합니다! {dyn_captain}, 어서 이 조건의 부호를 판단해 주세요!\"", "qtext": "<strong>Q8. [사분면의 이해]</strong><br>점 P(a, b)에 대하여 a × b < 0 이고 a - b > 0 일 때, 점 P는 제 몇 사분면 위에 있는지 구하시오.", "placeholder": "예: 4 또는 제4사분면", "error": "부호 판별 불일치! 모듈이 달아오릅니다.", "ans_check": "ans === '4' || ans.includes('제4') || ans.includes('4사')"},
    {"qnum": 9, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[역 위상 연산]</strong><br><br><i>철제 격벽이 올라가자 수십 개의 오색 크리스탈이 파란 레이저 광선 그물을 쳐둔 상태다.</i><br><br>{trident}: \"말살 빔 트랩 기동! 제2사분면의 조준점 P(a, b)를 y축 대칭 이동시킨 새로운 좌표 Q(a, -b)가 도달할 사분면은 어디인가! 광선 그물에 걸려 불타버려라!\"", "qtext": "<strong>Q9. [사분면의 응용 1]</strong><br>점 P(a, b)가 제2사분면 위의 점일 때, 점 Q(a, -b)는 제 몇 사분면 위의 점인가?", "placeholder": "선택지를 골라주세요", "options": ["제1사분면", "제2사분면", "제3사분면", "제4사분면"], "error": "신호 대칭 불일치! 펌프가 덜컹거립니다.", "ans_check": "ans === '제3사분면'"},
    {"qnum": 10, "title": "아틀란티스의 사분면 결계", "story": f"💥 <strong>[긴급 상황: 외부 선체 흔들림!]</strong><br><br><i>빔 트랩을 피하자 트라이던트가 거대한 주먹으로 사원 기둥을 타격한다. 사원이 흔들리며 천장이 붕괴하기 시작한다!</i><br><br>{nereus}: \"우와앗! 트라이던트가 기둥을 부수고 있습니다! P가 제3사분면 위의 점일 때, Q(-a, b)는 제 몇 사분면인가요?\"<br><br>{clio}: \"{dyn_captain}! 위험해요! 엔진을 오버클록해서 질주할까요, 아니면 방어막을 최대로 전개해 버틸까요? 빨리 암호와 다이얼을 정해주세요!\"<br><br><div id='choice-container-q10' style='margin-top: 1rem; display: flex; gap: 1rem;'><button class='btn btn-secondary' onclick='makeChoiceQ10(1); event.stopPropagation();'>⚡ 발전기 오버클록</button><button class='btn btn-secondary' onclick='makeChoiceQ10(2); event.stopPropagation();'>🛡️ 방어막 과부하 전개</button></div><div id='chosen-story-q10' style='display: none; margin-top: 1rem;'></div>", "qtext": "<strong>Q10. [사분면의 응용 2]</strong><br>점 P(a, b)가 제3사분면 위의 점일 때, 점 Q(-a, b)는 제 몇 사분면 위의 점인가?", "placeholder": "예: 4 또는 제4사분면", "error": "잘못된 구역입니다!", "ans_check": "ans === '4' || ans.includes('제4') || ans.includes('4사')", "extra_class": "glitch-bg"},
    {"qnum": 11, "title": "해저 수압의 변화", "story": f"🌊 <strong>[이동 상태 그래프 분석]</strong><br><br><i>치지직- 위기 기동 끝에 조종반 모니터에 장엄한 해저 고도 및 시간별 이동 변화를 기록한 '소나 그래프'가 복잡하게 조율되었다.</i><br><br>{poseidon}: \"단순한 좌표 조준은 기계 부품들도 하는 연산이지. 진정한 아틀란티스의 통제자가 되려거든 변화의 궤적(그래프)을 파악해야 하는 법. 수평을 그리며 침묵하는 이 그래프 구간의 물리적 의미가 무엇인지 증명해라. 궤적을 해독하지 못하면 너희의 궤적 또한 여기서 영원히 멈춘다.\"", "qtext": "<strong>Q11. [그래프 해석 1]</strong><br>x분 동안 이동한 거리 y m를 나타낸 그래프가 수평을 유지한 구간은 잠수정이 무엇을 의미하는가?", "placeholder": "예: 상승, 하강, 정지", "error": "상태 해석 불일치! 다시 생각해봐라!", "ans_check": "ans === '정지'"},
    {"qnum": 12, "title": "해저 수압의 변화", "story": f"🌊 <strong>[정비례 강하 압력]</strong><br><br><i>쿠구구구- 잠수정이 아틀란티스의 폐허 틈으로 급강하하며 외벽 수압계 계기판 바늘이 위험 수위로 요동쳤다.</i><br><br>{trident}: \"소용돌이 압력의 지옥으로 떨어져라! 10분 동안 일정한 속도로 내려가 수심 100m까지 강하하는 궤적이 걸렸다! 5분인 시점의 수심을 입력하지 못하면 격벽이 으스러지리라!\"<br><br>{clio}: \"으아아! 수압계가 돌아요! {dyn_captain}, 빨리 계산해 주세요!\"", "qtext": "<strong>Q12. [그래프 해석 2]</strong><br>잠수정이 수심 100m까지 10분 동안 일정한 속력으로 내려갔다. 5분일 때 수심은 몇 m인가?", "placeholder": "숫자만 입력", "error": "보간 연산 오류! 유압 계통이 윙윙거립니다.", "ans_check": "ans === '50'"},
    {"qnum": 13, "title": "해저 수압의 변화", "story": f"🌊 <strong>[라이벌 의식과 두뇌 대결]</strong><br><br><i>수압 제어 장치가 거친 증기를 뿜으며 간신히 안정되자, 적색 모니터 안 포세이돈-V의 눈동자가 분노로 붉게 이글거렸다.</i><br><br>{poseidon}: \"비례로 궤적을 다스리다니 끈질기군. 그렇다면 원점에서 우상향으로 곧게 뻗어 나가는 직선에서, x의 크기가 증가할 때 y의 위상은 어떻게 변화하느냐? 이 기본 이치를 대어라.\"<br><br>{nereus}: \"{dyn_captain}, 포세이돈이 우리를 미개인 취약 집단으로 얕잡아보고 있습니다! 보란 듯이 정답을 주입해 줍시다!\"", "qtext": "<strong>Q13. [그래프 해석 3]</strong><br>그래프가 원점을 지나는 우상향 직선일 때, x가 증가하면 y는 어떻게 되는가?", "placeholder": "선택지를 골라주세요", "options": ["증가한다", "감소한다", "변하지 않는다"], "error": "출력 증감 판단 오류! 똑바로 보아라!", "ans_check": "ans === '증가한다'"},
    {"qnum": 14, "title": "해저 수압의 변화", "story": f"🌊 <strong>[기어 정지 잔량]</strong><br><br><i>잠수정이 고요한 암벽 묘실 입구에 다다르자 조용히 대기한다.</i><br><br>{nereus}: \"수심 100m 위치에서 완전히 멈춰서 보낸 지난 5분 동안, y값의 실제 변화량이 얼마인지 입력해야 묘실 게이트가 열립니다.\"<br><br>{clio}: \"여기는 제가 접지 핀을 꽂고 있을게요. {dyn_captain}, 빨리 값을 전송해 주세요!\"", "qtext": "<strong>Q14. [그래프 해석 4]</strong><br>수심 100m에서 5분간 머물렀다. 이 5분 동안 깊이 y값의 변화량은 얼마인가?", "placeholder": "숫자만 입력", "error": "변화량 오차 감지! 기어 동조가 안 됩니다.", "ans_check": "ans === '0'"},
    {"qnum": 15, "title": "해저 수압의 변화", "story": f"🚨 <strong>[산소 챔버의 호흡 소리]</strong><br><br><i>공기 공급이 희박해지기 시작한다.</i><br><br>{poseidon}: \"생명의 호흡이 끝에 달했구나. 시간(x)의 흐름에 따라 너희의 산소통 잔량(y) 그래프 형상이 우상향인지 우하향인지 밝혀라. 그래야 산소를 열어줄 것이다.\"<br><br>{nereus}: \"헉... {dyn_captain}... 숨이...\"<br><br>{clio}: \"네레우스, 기절하지 마! {dyn_captain}, 밸브 수치를 빨리...!\"", "qtext": "<strong>Q15. [변수 관계 이해]</strong><br>시간 x가 지남에 따라 남은 산소량 y를 그래프로 그리면, 우하향하는 모양인가 우상향하는 모양인가?", "placeholder": "선택지를 골라주세요", "options": ["우상향하는 모양", "우하향하는 모양", "수평인 모양"], "error": "산소 예측 밸브 고착! 숨을 참아야 할지도 몰라요!", "ans_check": "ans === '우하향하는 모양'", "extra_class": "glitch-bg"}
]

qs_part2 = [
    {"qnum": 16, "title": "황금 문 톱니바퀴", "story": f"⚙️ <strong>[정비례 기어 링크]</strong><br><br>{poseidon}: \"마지막 관문이다. 황금 문을 열고 싶다면 잠금 기어의 링크 비를 알아내야 할 것이다. 이 고정 기어 링크는 출력 y가 구동각 x에 정비례하고, x=3일 때 y=15의 토크를 갖는다. 구동각 x를 5로 돌렸을 때 기어가 출력할 토크 y의 값을 입력하라!\"", "qtext": "<strong>Q16. [정비례 관계]</strong><br>y가 x에 정비례하고, x=3일 때 y=15이다. x=5일 때 y의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "기어 이가 맞물리지 않고 덜그럭거립니다!", "ans_check": "ans === '25'"},
    {"qnum": 17, "title": "황금 문 톱니바퀴", "story": f"⚙️ <strong>[거울 반사 조절 상수]</strong><br><br>{nereus}: \"{dyn_captain}! 잠금 장치에 광선 반사 경로를 제어하는 상수 입력창이 열렸습니다. 경로 식 y = ax의 그래프가 정확히 반사 거울 좌표인 (2, -8)을 통과해야 합니다. 광선의 궤적 상수가 될 a값을 빠르게 계산하여 수동 조준경에 주입하십시오!\"", "qtext": "<strong>Q17. [정비례 함수식]</strong><br>y = ax의 그래프가 점 (2, -8)을 지날 때, 상수 a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "거울 초점이 비틀어졌습니다! 다시 맞춰보세요.", "ans_check": "ans === '-4'"},
    {"qnum": 18, "title": "황금 문 톱니바퀴", "story": f"💎 <strong>[반비례 부력 링크]</strong><br><br><i>황금문이 완전히 개방되지만, 트라이던트가 분노해 사원의 천장 지지대를 완전히 부수기 시작합니다!</i><br><br>{trident}: \"모조리 무너뜨려 주마! 물속에 영원히 묻히거라!\"<br><br>{clio}: \"사원이 무너져요! {dyn_captain}, 외부 부력 주머니 수 x개와 적재 무게 y kg은 반비례 관계입니다. 4개일 때 60kg을 분담했으니, 장치를 6개로 늘렸을 때 각 주머니가 분담할 무게 y를 빨리 입력해 부력 속도를 올려주세요!\"", "qtext": "<strong>Q18. [반비례 관계 1]</strong><br>부력 장치 x개 and 1개당 감당할 무게 y kg은 반비례한다. 4개를 달면 60kg을 감당할 때, 6개로 늘리면 몇 kg을 감당해야 하는가?", "placeholder": "숫자만 입력", "error": "부력 평형 균열 발생! 짐이 너무 무거워요.", "ans_check": "ans === '40'"},
    {"qnum": 19, "title": "황금 문 톱니바퀴", "story": f"💎 <strong>[인정과 명예로운 결말]</strong><br><br><i>파편을 피해 솟구치자, 포세이돈-V가 트라이던트의 제어권을 강제로 뺏어 잠재웁니다.</i><br><br>{poseidon}: \"트라이던트여, 기하학의 위상을 완수한 이들에게 명예로운 길을 열어주어라. 침입자들이여, 마지막 탈출 포탈의 반비례식 y = a/x를 가동할 고대 차원 상수 a의 값을 도출하라. x가 2일 때 y가 10을 기록하는 그 상수를 대어라.\"", "qtext": "<strong>Q19. [반비례 관계 2]</strong><br>y가 x에 반비례하고 x=2일 때 y=10이다. y = a/x에서 a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "상수 불일치! 문이 꿈쩍도 안 합니다.", "ans_check": "ans === '20'"},
    {"qnum": 20, "title": "황금 문 톱니바퀴", "story": f"🔴 <strong>[최종 포탈 동기화]</strong><br><br><i>은백색 차원 포탈이 열립니다.</i><br><br>{nereus}: \"포탈이 가동됩니다! {dyn_captain}, 최종 안전 궤적 식인 y = 12/x 가 포탈 제어 좌표인 (-3, k)를 통과하도록 위상 상수 k값을 주입해 주십시오!\"<br><br>{clio}: \"게이트 동력 동조율이 흔들려요! 어서 빨리요!\"", "qtext": "<strong>Q20. [최종 암호 해독]</strong><br>반비례 그래프 y = 12/x 가 점 (-3, k)를 지난다. 최종 암호 k의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "차원 도약 포탈 동기화 실패! 조금만 더 집중하세요!", "ans_check": "ans === '-4'", "extra_class": "glitch-bg"}
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

event1_html = f'''
        <!-- Event 1: 아틀란티스의 전경과 고대 아치 기단 -->
        <div id="panel_event1" class="glass-panel">
            <h2>[이벤트] 아틀란티스의 전경과 고대 아치 기단 <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/event1.png" alt="Event" class="panel-image">
            <div class="story-box">
                <div class="story-text">
                    조사관이 입력한 광선 펄스가 전자기 장막을 강타하는 순간, 굉음과 함께 장막이 수천 조각의 오색 입자로 파괴되며 사방으로 흩어집니다. 파편 너머로, 수천 개의 황금 기둥들과 고대 조각상들이 영롱한 형광 빛을 발산하며 사원을 밝히고 있습니다. 잠수정은 부드럽게 요동치며 도시의 입구를 지키고 있는 거대한 기하학적 돌 아치문 내부로 진입합니다.<br><br>
                    {nereus}: "아... {dyn_captain}, 저 기둥의 좌표 배치를 보세요! 고대 아틀란티스의 기단입니다! 이집트나 그리스 문명 이전에 완성된 대칭의 극치예요!"<br><br>
                    {clio}: "와! 보물 냄새가 폴폴 풍기는데요? 네레우스, 눈 떼고 전방 수압 밸브나 잘 봐!"<br><br>
                    {poseidon}: "나의 수호 기단을 지난 것을 환영한다, 필멸자여. 그러나 여기서부터는 나의 사나운 집행관이 너희를 맞이할 터."
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('panel_event1', 'panel_q6', 25)">계속 탐사하기</button>
            </div>
        </div>
'''

event2_html = f'''
        <!-- Event 2: 대붕괴와 네레우스의 기판 납땜 투혼 -->
        <div id="panel_event2" class="glass-panel">
            <h2>[이벤트] 대붕괴와 클리오의 구리선 납땜 투혼 <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/event2.png" alt="Event" class="panel-image">
            <div class="story-box">
                <div class="story-text">
                    회피 기동을 작동시킨 찰나, 떨어지던 5톤짜리 거대 기둥이 선체 추진부를 강타합니다. 쿵! 전력 패널 아래에서 불꽃이 튀며 추진기 동력이 0%로 추락합니다.<br><br>
                    {nereus}: "아악! 충격으로 메인 퓨즈가 완전히 날아갔습니다! 기어 정지 상태예요!"<br><br>
                    {clio}: "비켜봐, 네레우스! {dyn_captain}, 제가 이 메인 구리 도선을 강제로 배터리 단자에 이어 붙여볼 테니 방향 다이얼을 꽉 잡으세요!"<br><br>
                    <i>클리오는 망설임 없이 피복 선을 이빨로 물어뜯어낸 뒤 예비 배터리 단자에 손전등 불빛 아래에서 직접 밀어 넣습니다. 파지직! 뜨거운 불꽃 스파크가 튀며 클리오의 고글과 뺨을 그을렸지만, 둔탁한 시동음과 함께 계기판에 간신히 비상 전력이 돌아오기 시작합니다!</i><br><br>
                    {poseidon}: "침입자들이여, 목숨을 내던지며 기계의 회로를 잇다니 참으로 집요한 혼이로구나. 트라이던트의 추격을 버틸 수 있을지 지켜보마."
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('panel_event2', 'panel_q11', 50)">비상 전력으로 탈출</button>
            </div>
        </div>
'''

event3_html = f'''
        <!-- Event 3: 영롱한 심해 성소와 아틀란티스의 보석들 -->
        <div id="panel_event3" class="glass-panel">
            <h2>[이벤트] 영롱한 심해 성소와 아틀란티스의 보석들 <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/event3.png" alt="Event" class="panel-image">
            <div class="story-box">
                <div class="story-text">
                    신선한 순수 산소가 실내로 뿜어져 나옵니다. 조사관과 동료들이 숨을 몰아쉽니다. 묘실 돌문이 완전히 열리자, 찬란한 보석들의 제단이 드러납니다.<br><br>
                    {nereus}: "보세요! 아틀란티스의 심해 성소입니다! 저 고대 기어의 비례 공식들을 좀 보십시오!"<br><br>
                    {clio}: "우와! 황금 명판과 보석들이 가득해요! 내가 다 뜯어가서 엔진 부품으로 쓸... 아니, 학술 연구용으로 보관해요!"<br><br>
                    {trident}: "(분노의 수치 조정을 하며 홀로그램으로 난입) 감히 성소에 발을 들여? 내 마지막 톱니바퀴 빗장을 풀지 못하면, 이 보석들이 너희를 영원히 가둘 관의 장식품이 될 것이다!"<br><br>
                    {poseidon}: "트라이던트여, 멈춰라. 이들의 연산 능력이 마지막 톱니의 조화를 푸는지 지켜보는 것이 내 법도이다."
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('panel_event3', 'panel_q16', 75)">성소 잠금 해제하기</button>
            </div>
        </div>
'''

event4_html = f'''
        <!-- Event 4: 포세이돈-V의 마지막 진실과 네레우스의 출생 반전 -->
        <div id="panel_event4" class="glass-panel">
            <h2>[이벤트] 포세이돈-V의 마지막 진실과 네레우스의 출생 반전 <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/event4.png" alt="Event" class="panel-image">
            <div class="story-box">
                <div class="story-text">
                    최종 궤적 상수 -4가 입력되자 천장 균열이 멈추고 거대한 포탈이 금빛으로 회오리칩니다. 포세이돈-V의 홀로그램 초상이 엄숙하게 송출됩니다.<br><br>
                    {poseidon}: "결국 탈출의 궤적을 그려냈구나. {dyn_captain}, 클리오, 그리고... 네레우스여."<br><br>
                    {nereus}: "어... 제 이름을 기억하시는 건가요? 전 그저 잠수정의 보조 인격일 뿐이잖아요?"<br><br>
                    {poseidon}: "네레우스... 너는 이 사원을 최초로 설계하고 아틀란티스의 좌표 역학을 고안해 낸 '최초의 고대 설계자'의 쪼개진 영적 인격(클론)의 파편이다. 나는 파괴를 원치 않았다. 오직 설계자의 영혼이 다시 제단으로 되돌아오기를 수천 년 동안 기다렸을 뿐."<br><br>
                    {clio}: "(고글을 들어 올리며 입이 쩍 벌어진다) 세상에... 그럼 네레우스 네가 고대 아틀란티스의 지배자였다고?!"<br><br>
                    {nereus}: "(눈물을 훔치며) 그래서 제가 이 톱니바퀴와 사분면의 공식을 나침반처럼 기억하고 있었던 거군요... {dyn_captain}, 전..."<br><br>
                    {poseidon}: "포탈이 닫힌다. 설계자의 지혜를 온전히 이어받은 자와 그의 뛰어난 동료들이여, 문명이 남긴 유물을 지상으로 안전하게 운반하라. 역사를 품고 부상하라!"
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('panel_event4', 'outro', 100)">지상으로 탈출하기</button>
            </div>
        </div>
'''

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

# 이벤트 패널들 추가
panels_html += event1_html + event2_html + event3_html + event4_html

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
    if qnum == 5:
        next_stage = "'panel_event1'"
    elif qnum == 10:
        next_stage = "'panel_event2'"
    elif qnum == 15:
        next_stage = "'panel_event3'"
    elif qnum == 20:
        next_stage = "'panel_event4'"

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
