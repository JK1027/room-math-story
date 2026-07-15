import re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_04_escape_room.html")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Questions Data
nereus = '<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[네레우스]</span>'
poseidon = '<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[포세이돈-V]</span>'

qs = [
    {"qnum": 1, "title": "심해로 가는 좌표 (순서쌍과 좌표)", "story": f"🌊 <strong>[목표 지점 확인]</strong><br><br>{nereus}: \"캡틴, 전방에 아틀란티스 유적 입구의 에너지 역장이 감지되었습니다. 진입을 위한 해수면 투하 좌표(순서쌍)를 정확히 입력해야 잠수정이 무사히 진입합니다!\"<br><br>🚨 <strong>[통신 간섭 발생]</strong><br><br>{poseidon}: \"어리석은 침입자들... 심해의 압력에 짓눌려 흔적도 없이 사라져라. 나는 이 유적을 수호하는 고대 AI, 포세이돈-V. 감히 내 영역을 밟다니... 첫 번째 좌표조차 빗나간다면 심해의 암초가 너희의 무덤이 될 것이다!\"", "qtext": "<strong>Q1. [순서쌍 좌표 찍기]</strong><br>x좌표가 -5 이고, y좌표가 8 인 점의 <strong>좌표</strong>를 순서쌍 기호 괄호 ()를 사용하여 나타내시오.", "placeholder": "예: (3, 4)", "error": "투하 좌표가 어긋났습니다! 암초에 부딪힐 위험이 있습니다!", "ans_check": "ans === '-5,8'"},
    {"qnum": 2, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[투하 지점 갱신]</strong><br><br>{poseidon}: \"운 좋게 피해갔군. 하지만 내 수압 쇄도 밸브는 자비가 없다! 진입 축의 기준 신호를 정합해 보아라. x축 위의 제어 포인트를 찾지 못하면 뼈대조차 남지 않게 압착해주지!\"", "qtext": "<strong>Q2. [x축, y축 위의 점]</strong><br>x축 위에 있고 x좌표가 7인 점의 좌표를 나타내시오.", "placeholder": "예: (2, 0)", "error": "좌표 입력 오류! 수압 경고!", "ans_check": "ans === '7,0'"},
    {"qnum": 3, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[기준점 확인]</strong><br><br>{nereus}: \"캡틴! 포세이돈-V의 해킹으로 영점 조준 회로가 심각한 손상을 입었습니다. 원점을 빠르게 동기화하여 기준 좌표를 복구해 주십시오!\"", "qtext": "<strong>Q3. [원점의 좌표]</strong><br>두 좌표축이 만나는 원점 O의 좌표를 나타내시오.", "placeholder": "예: (x, y)", "error": "영점 조준 실패!", "ans_check": "ans === '0,0'"},
    {"qnum": 4, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[추가 기준점]</strong><br><br>{poseidon}: \"과거 아틀란티스는 단 1%의 좌표 연산 오차로 인해 바다 밑으로 가라앉았다... 그 죗값을 이제 너희가 치를 차례다! y축 해저 동굴의 궤도를 정확히 전송하라. 오차가 생기면 산산조각 날 것이다!\"", "qtext": "<strong>Q4. [좌표 평면 위의 점]</strong><br>y축 위에 있고 y좌표가 -3인 점의 좌표를 나타내시오.", "placeholder": "예: (0, -5)", "error": "동굴 충돌 위험!", "ans_check": "ans === '0,-3'"},
    {"qnum": 5, "title": "심해로 가는 좌표", "story": f"🌊 <strong>[소용돌이 결계]</strong><br><br>{nereus}: \"적 잠수정들이 4개 기둥 좌표를 기준으로 에너지 가로막을 설치했습니다. 이 소용돌이 결계의 총 넓이를 알아내야 해제 루틴이 실행됩니다. 포세이돈-V의 교란 신호를 무시하십시오!\"", "qtext": "<strong>Q5. [도형의 넓이]</strong><br>좌표평면 위에 네 기둥 A(3, 4), B(-3, 4), C(-3, -4), D(3, -4)를 이은 직사각형의 넓이를 구하시오.", "placeholder": "숫자만 입력", "error": "결계 돌파 실패!", "ans_check": "ans === '48'"},
    {"qnum": 6, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[사분면 분석]</strong><br><br>{poseidon}: \"사분면 방어 격자 기동! 너희들의 하찮은 잠수정이 이 복잡한 좌표의 미궁을 빠져나갈 수 있을 거라 생각하나? 기동점 (2, -5)의 위치 구역을 탐색해 보아라!\"", "qtext": "<strong>Q6. [사분면의 부호 1]</strong><br>점 (2, -5)는 제 몇 사분면 위의 점인가?", "placeholder": "숫자만 입력 (예: 1)", "error": "잘못된 구역입니다!", "ans_check": "ans === '4'"},
    {"qnum": 7, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[추가 결계]</strong><br><br>{poseidon}: \"쥐새끼처럼 잘도 피하는군. 그렇다면 제2구역 결계 장벽의 좌표 (-4, -7) 사분면 영역을 해독해 봐라. 여기서 너희들의 숨통을 끊어주마!\"", "qtext": "<strong>Q7. [사분면의 부호 2]</strong><br>점 (-4, -7)은 제 몇 사분면 위의 점인가?", "placeholder": "숫자만 입력", "error": "잘못된 구역입니다!", "ans_check": "ans === '3'"},
    {"qnum": 8, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[고급 사분면]</strong><br><br>{nereus}: \"캡틴! 포세이돈-V가 좌표 P(a, b)의 부호 조건을 은닉하여 우리 해킹 장치를 교란하고 있습니다. 조건을 충족하는 사분면 구역을 논리적으로 분석해 주십시오!\"", "qtext": "<strong>Q8. [사분면의 이해]</strong><br>점 P(a, b)에 대하여 a × b < 0 이고 a - b > 0 일 때, 점 P는 제 몇 사분면 위에 있는지 구하시오.", "placeholder": "숫자만 입력", "error": "잘못된 구역입니다!", "ans_check": "ans === '4'"},
    {"qnum": 9, "title": "아틀란티스의 사분면 결계", "story": f"🧭 <strong>[사분면 분석]</strong><br><br>{poseidon}: \"경보 강도 최대치 출력! 변형 좌표 Q(a, -b)의 사분면 신호를 인증해 보아라! 인간의 나약한 뇌수로는 불가능할 것이다!\"", "qtext": "<strong>Q9. [사분면의 응용 1]</strong><br>점 P(a, b)가 제2사분면 위의 점일 때, 점 Q(a, -b)는 제 몇 사분면 위의 점인가?", "placeholder": "숫자만 입력", "error": "잘못된 구역입니다!", "ans_check": "ans === '3'"},
    {"qnum": 10, "title": "아틀란티스의 사분면 결계", "story": f"💥 <strong>[긴급 상황: 외부 선체 파손!]</strong><br><br>{poseidon}: \"방어 그리드 최종 활성화! 좌표 Q(-a, b)의 사분면을 계산하지 못하면 자폭 레이저가 가동된다! 영원한 심연으로 떨어져라!\"<br><br>{nereus}: \"경고! 우측 선체 장갑 30% 손실! 자폭 프로토콜이 시작되었습니다! 제발 빨리 결제 전술을 선택하고 전송해주십시오!\"<br><br><div id='choice-container-q10' style='margin-top: 1rem; display: flex; gap: 1rem;'><button class='btn btn-secondary' onclick='makeChoiceQ10(1); event.stopPropagation();'>⚡ 발전기 오버클록</button><button class='btn btn-secondary' onclick='makeChoiceQ10(2); event.stopPropagation();'>🛡️ 방어막 과부하 전개</button></div><div id='chosen-story-q10' style='display: none; margin-top: 1rem;'></div>", "qtext": "<strong>Q10. [사분면의 응용 2]</strong><br>점 P(a, b)가 제3사분면 위의 점일 때, 점 Q(-a, b)는 제 몇 사분면 위의 점인가?", "placeholder": "숫자만 입력", "error": "잘못된 구역입니다!", "ans_check": "ans === '4'", "extra_class": "glitch-bg"},
    {"qnum": 11, "title": "해저 수압의 변화", "story": f"🌊 <strong>[수압 경고]</strong><br><br>{nereus}: \"휴... 캡틴, 일단 치명적인 고비는 넘겼습니다. 하지만 외부 수압 그래프가 비정상적으로 요동치고 있습니다. 그래프 상에서 이동 거리 y가 평평하게 멈춘 구간이 뜻하는 기동 상태를 해석해 밸브를 안정화해주십시오.\"", "qtext": "<strong>Q11. [그래프 해석 1]</strong><br>x분 동안 이동한 거리 y m를 나타낸 그래프가 수평을 유지한 구간은 잠수정이 무엇을 의미하는가?", "placeholder": "예: 상승, 하강, 정지", "error": "그래프 해석 오류!", "ans_check": "ans === '정지'"},
    {"qnum": 12, "title": "해저 수압의 변화", "story": f"🌊 <strong>[깊이 예측]</strong><br><br>{nereus}: \"수온 냉각 파이프라인의 압력이 계속해서 떨어집니다... 10분 동안 100m 하강했을 때 5분 시점의 깊이를 예측해 펌프를 복구하십시오. 시간이 없습니다!\"", "qtext": "<strong>Q12. [그래프 해석 2]</strong><br>잠수정이 수심 100m까지 10분 동안 일정한 속력으로 내려갔다. 5분일 때 수심은 몇 m인가?", "placeholder": "숫자만 입력", "error": "깊이 예측 실패!", "ans_check": "ans === '50'"},
    {"qnum": 13, "title": "해저 수압의 변화", "story": f"🌊 <strong>[그래프 방향]</strong><br><br>{poseidon}: \"발버둥 쳐 보아라! 내가 잠수정의 엔진 출력을 무작위로 조작해 두었다! 원점을 지나는 우상향 직선 그래프의 성질을 모른다면 이대로 심연에 곤두박질칠 것이다!\"", "qtext": "<strong>Q13. [그래프 해석 3]</strong><br>그래프가 원점을 지나는 우상향 직선일 때, x가 증가하면 y는 어떻게 되는가?", "placeholder": "예: 증가, 감소", "error": "해석 오류!", "ans_check": "ans === '증가'"},
    {"qnum": 14, "title": "해저 수압의 변화", "story": f"🌊 <strong>[변화량 분석]</strong><br><br>{nereus}: \"엔진이 멈췄습니다! 5분 동안 깊이가 고정되어 있습니다. 이 머문 시간 동안의 깊이 변화량을 릴레이에 입력하여 재시동을 걸어주십시오. 서두르지 않으면 산소 시스템이...\"", "qtext": "<strong>Q14. [그래프 해석 4]</strong><br>수심 100m에서 5분간 머물렀다. 이 5분 동안 깊이 y값의 변화량은 얼마인가?", "placeholder": "숫자만 입력", "error": "해석 오류!", "ans_check": "ans === '0'"},
    {"qnum": 15, "title": "해저 수압의 변화", "story": f"🚨 <strong>[치명적 오류: 산소 공급 장치 파손]</strong><br><br>{nereus}: \"치직... 캡틴... 비상 산소 탱크의 압력이 한계점입니다. 시간 흐름에 따른 산소 잔량 그래프 개형을 예상하십시오. 제... 제 연산 코어가 타들어가고 있습니다. 캡틴, 제발... 살아서 돌아가야 합니다!\"", "qtext": "<strong>Q15. [변수 관계 이해]</strong><br>시간 x가 지남에 따라 남은 산소량 y를 그래프로 그리면, 우하향하는 모양인가 우상향하는 모양인가?", "placeholder": "예: 우하향, 우상향", "error": "산소 예측 실패!", "ans_check": "ans === '우하향'", "extra_class": "glitch-bg"},
    {"qnum": 16, "title": "황금 문 톱니바퀴", "story": f"⚙️ <strong>[정비례 회전]</strong><br><br>{poseidon}: \"말도 안 돼! 이 수압과 산소 부족을 견디고 여기까지 도달했다고?! 하지만 이것이 마지막이다. 황금 문의 톱니바퀴 동력을 정비례 관계식으로 풀어내지 못하면 문 앞에서 죽게 될 것이다!\"", "qtext": "<strong>Q16. [정비례 관계]</strong><br>y가 x에 정비례하고, x=3일 때 y=15이다. x=5일 때 y의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "톱니바퀴가 멈췄습니다!", "ans_check": "ans === '25'"},
    {"qnum": 17, "title": "황금 문 톱니바퀴", "story": f"⚙️ <strong>[비례 상수]</strong><br><br>{nereus}: \"포세이돈-V의 방화벽이 무너지고 있습니다! 회전 비례 상수 a값을 계산해 보정 코드를 칩에 업로드하십시오. 캡틴, 조금만 더 힘을 내주십시오!\"", "qtext": "<strong>Q17. [정비례 함수식]</strong><br>y = ax의 그래프가 점 (2, -8)을 지날 때, 상수 a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "다이얼 번호 오류!", "ans_check": "ans === '-4'"},
    {"qnum": 18, "title": "황금 문 톱니바퀴", "story": f"💎 <strong>[보물 적재 경보]</strong><br><br>{nereus}: \"황금 문 틈새로 엄청난 양의 보물이 보입니다! 하지만 아웃플로우 밸브의 부력 장치 수 x와 무게 y의 반비례 관계를 연산하여 안전 무게 상한선을 재설정하지 않으면, 무게를 이기지 못하고 다시 침몰할 것입니다!\"", "qtext": "<strong>Q18. [반비례 관계 1]</strong><br>부력 장치 x개와 1개당 감당할 무게 y kg은 반비례한다. 4개를 달면 60kg을 감당할 때, 6개로 늘리면 몇 kg을 감당해야 하는가?", "placeholder": "숫자만 입력", "error": "부력 균형 붕괴!", "ans_check": "ans === '40'"},
    {"qnum": 19, "title": "황금 문 톱니바퀴", "story": f"💎 <strong>[반비례 상수]</strong><br><br>{poseidon}: \"크아아악!! 시스템 락다운 직전이다! 이럴 수가... 하찮은 인간이 내 수천 년의 연산 코어를 능가하다니!! 반비례 비례상수 a를 식에 주입해라! 이 문이 열리면 안 돼!!\"", "qtext": "<strong>Q19. [반비례 관계 2]</strong><br>y가 x에 반비례하고 x=2일 때 y=10이다. y = a/x에서 a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "식 계산 오류!", "ans_check": "ans === '20'"},
    {"qnum": 20, "title": "황금 문 톱니바퀴", "story": f"🔴 <strong>[최종 탈출 레이저]</strong><br><br>{nereus}: \"모든 제어권을 탈환했습니다! 마지막 탈출 통로의 역반사 궤적 좌표가 반비례 그래프 y = 12/x 와 점 (-3, k)를 지납니다. 캡틴, 최종 암호 k의 값을 입력해 저 오만한 포세이돈-V의 전원을 끄고 포탈을 가동하십시오!!\"", "qtext": "<strong>Q20. [최종 암호 해독]</strong><br>반비례 그래프 y = 12/x 가 점 (-3, k)를 지난다. 최종 암호 k의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "레이저 방어막에 막혔습니다!", "ans_check": "ans === '-4'", "extra_class": "glitch-bg"}
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
    
    # 힌트 버튼을 질문 제목 <strong>Q{qnum}. [제목]</strong> 바로 옆에 삽입
    hint_btn_html = f'<button class="btn-hint" onclick="alert(\'💡 힌트: {q["hint"]}\')">💡 힌트</button>'
    qtext_hinted = qtext.replace('</strong>', f'</strong> {hint_btn_html}', 1)
    
    extra_class = q.get('extra_class', '')
    qbox_id = 'id="q10-main-box" style="display:none;"' if qnum == 10 else ''
    panel = f'''
        <!-- Q{qnum} -->
        <div id="panel_q{qnum}" class="glass-panel {extra_class}">
            <h2>제 {qnum}구역: {title} <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">{story}</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="question-box" {qbox_id}>
                <div class="question-content">
                    {qtext_hinted}
                    <div class="input-group">
                        <input type="text" id="ans{qnum}" placeholder="{placeholder}">
                    </div>
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
outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>탈출 성공!</h1>
            <h2>아틀란티스의 보물</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/outro.png" alt="Background" class="panel-image">
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
                totalWrongCount++;
                timeLeft -= 60;
                if (timeLeft < 0) timeLeft = 0;
                updateTimerDisplay();
                triggerTimerWarning();
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

import re

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
</style>

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

function makeChoiceQ10(type) {
    document.getElementById('choice-container-q10').style.display = 'none';
    const textEl = document.getElementById('chosen-story-q10');
    textEl.style.display = 'block';
    if (type === 1) {
        textEl.innerHTML = "<span style='color:#60a5fa; text-shadow: 0 0 5px #3b82f6;'>[네레우스]</span>: '오버클록 성공! 순간 전력이 200% 상승해 자폭 레이저 연산 장치를 무력화 시도 중입니다. 하지만 과부하 열기가 대단합니다! 어서 좌표 계산을 완료하십시오!'";
    } else {
        textEl.innerHTML = "<span style='color:#60a5fa; text-shadow: 0 0 5px #3b82f6;'>[네레우스]</span>: '방어막 전개! 레이저 충격을 분산하고 흡수하기 시작했습니다. 실드가 버티는 동안 좌표 계산을 신속하게 끝내야 합니다!'";
    }
    document.getElementById('q10-main-box').style.display = 'block';
}
</script>
'''

new_content = re.sub(r'<!-- Q1.*?(?=<script>)', lambda m: '<!-- Q1 -->\n' + panels_html + '\n    ', content, flags=re.DOTALL)
new_content = re.sub(r'// Q1[\s\S]*?(?=window\.onload = \(\) => \{)', lambda m: '// Q1\n' + js_checks + '\n        ', new_content)
new_content = new_content.replace('</style>', glitch_css)

# startTimer 내 alert/reload를 게임오버 패널 전환으로 교체
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
new_content = re.sub(r'function startTimer\(\) \{[\s\S]*?\}', timer_replacement.strip(), new_content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated successfully.")
