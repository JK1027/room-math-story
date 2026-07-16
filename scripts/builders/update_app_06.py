# -*- coding: utf-8 -*-\nimport re

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_06_escape_room.html")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

qs = [
    {'qnum': 1, "options": ["팔각형", "팔각형 아님", "알 수 없음", "해 없음"], 'title': '거울 열 배분', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "크하하! 이 뜨거운 태양 신전은 내 거울 결계 지배하에 있다! 한 꼭짓점에서 5개의 대각선을 그릴 수 있는 다각형 문양을 맞춰 첫 거울을 작동시켜 봐라!"<br><br><i>지이잉- 천장의 황동 반사거울에서 레이저처럼 뜨거운 적색 빛줄기가 뿜어져 나오며 통로 바닥을 불태우기 시작합니다. 거울 각도를 분산시키기 위해 다각형 이름을 입력해야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "캡틴! 동력 시스템이 가동되었습니다! 다각형의 기하학 성질을 역이용해 대각선 정렬 각도를 맞춰 주십시오!" """, 'qtext': '<strong>Q1. [다각형의 대각선 1]</strong><br>한 꼭짓점에서 그을 수 있는 대각선의 개수가 5개인 다각형의 이름을 구하시오.', 'placeholder': '예: 육각형', 'error': '기둥 조작 오류!', 'ans_check': "ans === '팔각형'", 'hint': 'n각형의 한 꼭짓점에서 그을 수 있는 대각선의 개수 공식은 n-3 입니다.'},
    {'qnum': 2, "options": ["37", "33", "70", "35"], 'title': '기둥 교차망', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "거울 하나를 돌렸다고 안심하지 마라! 십각형 모양으로 배치된 내 기둥들의 교차 광선 그물이 네놈들의 탈출로를 완전히 차단할 것이다!"<br><br><i>십각형 형태로 늘어선 황동 기둥 끝에서 푸른 레이저 장벽이 거미줄처럼 엇갈리며 좁혀옵니다. 교차하는 모든 대각선 총 개수를 산출해 교차망을 무력화하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "캡틴! 기둥 사이의 모든 대각선 광선 가닥수를 구해 해독 펄스로 전송해야 합니다! 속도를 높여주십시오!" """, 'qtext': '<strong>Q2. [다각형의 대각선 2]</strong><br>십각형 모양의 기둥 배치에서 모든 기둥끼리 서로 빛을 교차 연결하려고 한다. 총 대각선의 개수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '계산 오류!', 'ans_check': "ans === '35'", 'hint': 'n각형의 총 대각선 수 공식인 n(n-3)/2 에 10을 대입하여 계산합니다.'},
    {'qnum': 3, "options": ["105", "103", "210", "107"], 'title': '빛의 반사각', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "기둥 교차망을 우회하다니 기특하군. 하지만 삼각형 반사판의 엇갈리는 세 각의 조화는 인간의 연산 한계를 초월한다!"<br><br><i>벽면의 삼각형 청동 거울판 각도가 뒤틀리며 레이저가 굴절되어 폭발을 일으키기 시작합니다. 두 내각의 정보로 나머지 한 꼭짓점의 외각 반사 수치를 찾아 정렬해야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "삼각형의 외각 반사 성질을 적용해 굴절 모터에 주입하십시오! 과부하로 렌즈가 깨지기 직전입니다!" """, 'qtext': '<strong>Q3. [삼각형의 외각 1]</strong><br>삼각형 반사판에서 두 내각이 각각 45도, 60도일 때, 나머지 한 내각의 외각의 크기를 구하시오.', 'placeholder': '숫자만 입력', 'error': '각도 오류!', 'ans_check': "ans === '105'", 'hint': '삼각형의 한 외각의 크기는 그와 이웃하지 않는 두 내각의 크기의 합과 같습니다.'},
    {'qnum': 4, "options": ["160", "162", "158", "320"], 'title': '외각의 배분', 'story': """<strong>[시스템 통신 장애 및 적색 플래시 경보]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "치지직... 캡틴! 세트-S의 해킹 펄스가 다각형 굴절 모터를 역제어해 폭주를 가속하고 있습니다! 삼각형의 세 외각 비율을 이용해 가장 강한 외각 출력을 상쇄할 비상 주입 각도를 산출해야 합니다! 서두르십시오!" """, 'qtext': '<strong>Q4. [삼각형의 외각 2]</strong><br>삼각형의 세 외각의 비가 2:3:4일 때, 가장 큰 외각의 크기를 구하시오.', 'placeholder': '숫자만 입력', 'error': '비율 오류!', 'ans_check': "ans === '160'", 'hint': '다각형의 외각의 총합은 항상 360도입니다. 비례배분을 이용하여 가장 큰 비율(4)을 차지하는 외각을 구합니다.'},
    {'qnum': 5, "options": ["5", "14", "7", "9"], 'title': '신전 내각 다이얼', 'story': """🚨 <strong>[격벽 압축 공기 배출 밸브 잠김 경보]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "치직... 제어 회로 복구율 45%! 신전 기하학 콘솔의 내각 총합이 900도인 다각형의 모서리(꼭짓점) 수만큼 핀을 정렬해야 산소 밸브가 열립니다! 조금만 힘을 내십시오!"<br><br><i>탁한 증기가 배출관에서 역류하며 숨쉬기가 힘들어지기 시작합니다.</i> """, 'qtext': '<strong>Q5. [다각형의 내각]</strong><br>내각의 크기의 합이 900도인 다각형의 꼭짓점의 개수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '다각형 모양 오류!', 'ans_check': "ans === '7'", 'hint': 'n각형의 내각의 총합 공식은 180 * (n-2) 입니다. 이 값이 900이 되는 n을 찾습니다.'},
    {'qnum': 6, "options": ["720", "362", "358", "360"], 'title': '외각의 법칙', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "하찮은 구식 메모리와 내통하다니 쓸데없는 발악이다! 어떤 다각형을 가져와도 결코 변하지 않는 외각의 불변의 법칙을 뚫어봐라!"<br><br><i>사방의 황동 벽면이 요동치며 여러 다각형 문양들이 어지럽게 떠오릅니다. 어떤 다각형이든 상관없이 외각의 절대 총합 각도를 입력해 락을 분해하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "캡틴! 기하학적으로 모든 다각형의 외각의 총합은 언제나 일정한 상수를 유지합니다. 그 수치를 다이얼에 주입하십시오!" """, 'qtext': '<strong>Q6. [다각형의 외각의 합]</strong><br>모든 다각형의 외각의 크기의 합은 항상 일정합니다. 그 크기는 몇 도인가?', 'placeholder': '숫자만 입력', 'error': '회전판이 멈췄습니다!', 'ans_check': "ans === '360'", 'hint': '다각형이 몇 각형이든 상관없이 모든 외각의 크기의 총합은 항상 360도입니다.'},
    {'qnum': 7, "options": ["정십각형", "정십각형 아님", "알 수 없음", "해 없음"], 'title': '정다각형의 추적', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "다이얼 문양을 제멋대로 분산시켰다. 한 외각의 각도가 36도인 정다각형을 추적해 그 이름을 입력하지 못하면 천장 거울이 붕괴하리라!"<br><br><i>천장에 매달린 대형 혼천의 반사경 프레임이 요란한 기계음과 함께 기울어집니다. 정확한 정다각형 명칭을 찾아 입력해야 정렬됩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "캡틴! 정다각형의 한 외각 크기가 36도가 되는 대상 다각형의 원래 한글 이름을 다이얼에 새겨 넣으십시오!" """, 'qtext': '<strong>Q7. [정다각형의 외각]</strong><br>한 외각의 크기가 36도인 정다각형의 이름을 구하시오.', 'placeholder': '예: 정오각형', 'error': '다이얼 문양 오류!', 'ans_check': "ans === '정십각형'", 'hint': '정n각형의 한 외각 크기는 360 / n 입니다. 이 값이 36이 되는 n을 구해 정다각형 이름을 적습니다.'},
    {'qnum': 8, "options": ["133", "137", "135", "270"], 'title': '블록 설계도', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "정팔각형 모양으로 짜인 거울 기둥의 내부 반사 경로를 계산할 지능이 네놈들에게 있느냐? 한 내각의 틈새 각도를 해독해 봐라!"<br><br><i>바닥에서 팔각형 청동 기둥이 솟아오르고, 빛이 정팔각형의 내벽을 따라 엇갈리게 굴절됩니다. 굴절 모터의 안전 반사각(정팔각형의 한 내각)을 정확히 입력하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "기둥이 뜨거워지고 있습니다! 정팔각형의 한 내각 크기를 구하여 모터에 동조시켜 주십시오!" """, 'qtext': '<strong>Q8. [정다각형의 내각 1]</strong><br>정팔각형의 한 내각의 크기를 구하시오.', 'placeholder': '숫자만 입력', 'error': '각도 입력 실패!', 'ans_check': "ans === '135'", 'hint': '정팔각형의 내각 총합인 180 * (8-2) = 1080도를 꼭짓점 개수인 8로 나누어 한 내각을 구합니다.'},
    {'qnum': 9, "options": ["52", "56", "108", "54"], 'title': '대각선 기어', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "좋다! 하지만 한 내각의 크기가 150도인 다면체 반사 기어의 모든 얽힘 대각선을 정렬하지 못하면, 거울들이 충돌해 전부 깨질 것이다!"<br><br><i>드르륵- 청동 콘솔 내부에서 톱니바퀴들이 어긋나며 거친 연기를 내뿜기 시작합니다. 조건에 부합하는 정다각형의 총 대각선 수치를 구해 동기화해 주어야 멈춥니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "비상! 기어 마모 한계 도달! 한 내각이 150도인 정다각형을 도출하고, 그 다각형의 대각선의 총개수를 즉시 입력하십시오!" """, 'qtext': '<strong>Q9. [정다각형의 내각 2]</strong><br>한 내각의 크기가 150도인 정다각형의 대각선의 총 개수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '계산 오류!', 'ans_check': "ans === '54'", 'hint': '한 내각이 150도이면 한 외각은 30도입니다. 외각의 합이 360도이므로 정십이각형임을 구한 뒤 총 대각선 공식을 적용합니다.'},
    {'qnum': 10, "options": ["정십각형", "정십각형 아님", "알 수 없음", "해 없음"], 'title': '비율 정렬', 'story': """💥 <strong>[비상 로그: 신전 냉각 시스템 파손 및 강제 자폭 작동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "더는 참을 수 없군! 모든 데이터를 소멸시키겠다! 5분 뒤 태양 코어의 에너지를 폭발시켜 이 지하 신전을 통째로 붕괴시키마!"<br><br><i>삐- 삐- 붉은 위급 경고가 뿜어져 나오며 중앙의 수조 덮개가 터져 뜨거운 증기가 가득 찹니다. 내각과 외각의 비가 4:1인 정다각형 이름을 해독해 비상 냉각 시스템을 가동해야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "캡틴! 시스템 온도가 한계치를 상회했습니다! 조건에 부합하는 정다각형 명칭을 입력하십시오! 제가 비상 방화벽으로 노심을 억제하겠습니다!" """, 'qtext': '<strong>Q10. [내각과 외각의 비]</strong><br>한 내각과 한 외각의 크기의 비가 4:1인 정다각형의 이름을 구하시오.', 'placeholder': '예: 정육각형', 'error': '암호판 고정 실패!', 'ans_check': "ans === '정십각형'", 'hint': '한 내각과 한 외각의 합은 180도입니다. 이를 4:1로 비례배분하여 한 외각을 구하고 다각형 이름을 유추합니다.', "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '제3구역 석판 봉인', 'story': """<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "방어막 출력 30%...! 캡틴, 코드를 연달아 입력해 열방출 포트를 지속 가동해야 합니다! ⚙️ [부채꼴 비례 제어]"<br><br><i>바닥의 거대한 원형 석판 문양이 스파크를 튀깁니다. 부채꼴의 호의 길이와 중심각의 수학적 상관관계를 정의해 석판 잠금을 해제하십시오.</i> """, 'qtext': '<strong>Q11. [호의 길이와 중심각 1]</strong><br>한 원에서 부채꼴의 호의 길이는 중심각의 크기에 어떻게 비례하는가?', 'placeholder': '예: 정비례, 반비례', 'error': '비례 원리 오류!', 'ans_check': "ans === '정비례'", 'hint': '부채꼴의 중심각이 커질 때 호의 길이도 이에 비례하여 일정하게 늘어나는 성질을 뜻합니다.'},
    {'qnum': 12, 'title': '길이 복사기', 'story': """<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "좋습니다, 비례 밸브를 열었으나 2차 배관의 수압이 맞지 않아 호스가 요동칩니다! ⚙️ [호의 길이 연산 복구]"<br><br><i>콸콸콸- 수조에 냉각수가 쏟아지며 수압 파이프가 격렬하게 떨립니다. 중심각과 호의 길이의 정비례 원리를 이용해 160도 대역의 정확한 호의 길이를 구해 주입하십시오!</i> """, 'qtext': '<strong>Q12. [호의 길이와 중심각 2]</strong><br>중심각이 40도일 때 호의 길이가 6cm라면, 중심각이 160도일 때 호의 길이를 구하시오.', 'placeholder': '숫자만 입력', 'error': '호의 길이 조절 실패!', 'ans_check': "ans === '24'", 'hint': '중심각의 크기와 호의 길이는 정비례하므로, 중심각이 4배 증가할 때 호의 길이도 똑같이 4배 증가합니다.'},
    {'qnum': 13, 'title': '지지대의 평형', 'story': """<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "엔진 온도가 진정되었습니다! 이제 중심 포탈을 향해 원의 넓이의 1/6을 차지하는 부채꼴 제어판의 각도를 맞추어야 합니다!"<br><br><i>안내 빔이 황금빛 각도판 위에 원의 1/6 영역을 가리키기 시작합니다. 이 영역의 정확한 중심각 수치를 입력해야 통로가 격리 벽에서 해제됩니다.</i> """, 'qtext': '<strong>Q13. [부채꼴의 넓이와 중심각]</strong><br>부채꼴의 넓이가 원의 넓이의 1/6일 때, 이 부채꼴의 중심각의 크기를 구하시오.', 'placeholder': '숫자만 입력', 'error': '각도 조절 실패!', 'ans_check': "ans === '60'", 'hint': '원 전체의 중심각 is 360도입니다. 넓이가 원의 1/6이므로 중심각도 360도의 1/6을 차지합니다.'},
    {'qnum': 14, 'title': '나무막대 기둥', 'story': """<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "치직... 중심각이 일치하는 두 부채꼴 궤도의 현(직선 도선)의 길이 관계식을 확인해, 엇갈리는 회로 위상을 매칭해 주십시오!"<br><br><i>두 교차 레이저 통로 아래에 파란 광섬유 링 두 개가 회전합니다. 두 부채꼴의 현의 길이 일치성에 대한 답을 입력하십시오.</i> """, 'qtext': '<strong>Q14. [현의 길이]</strong><br>중심각의 크기가 같은 두 부채꼴의 현의 길이는 서로 같은가?', 'placeholder': '예: 같다, 다르다', 'error': '현의 길이 오류!', 'ans_check': "ans === '같다'", 'hint': '중심각이 같은 두 부채꼴에서 원 위의 두 점을 곧게 이은 선분(현)의 길이를 비교해 봅니다.'},
    {'qnum': 15, 'title': '작도 판정', 'story': """✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A 신전 제어 권한 100% 완전 복구]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "해독 성공! 신전 메인 콘솔의 모든 제어권을 제가 완전히 흡수했습니다! 이제 세트-S의 바이러스 결계를 밀어내겠습니다. 현과 중심각의 진짜 비례 속성을 판정하여 전송하십시오!"<br><br><i>거울 장치들이 일제히 푸른색 마나 불꽃을 밝히며 부드럽게 정렬되기 시작합니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "내 핵심 락이 무력화당하다니...! 최종 원형 궤도 결계로 너희의 탈출을 저지하겠다!" """, 'qtext': '<strong>Q15. [현과 중심각의 비례]</strong><br>현의 길이는 중심각의 크기에 정비례하는가?', 'placeholder': '예: 그렇다, 아니다', 'error': '비례 관계 오류!', 'ans_check': "ans === '아니다'", 'hint': '중심각이 2배가 될 때 현의 길이도 정확히 2배가 되는지 원 위에 직접 그려 확인해 봅니다.', "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '제4구역 최종 냉각', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "마지막 결계까지 도달했나? 하지만 원형 포탈 테두리의 원주 에너지를 정확히 산출해내지 못하면 차원의 틈새에 갇혀 으스러지리라!"<br><br><i>지이잉- 거대 원형 포탈 테두리에 붉은 전류 스파크가 타오르며 수축을 시작합니다. 반지름 5cm 원형 포탈의 총 둘레 수치(원주)를 입력하여 포탈 크기를 강제로 고정하십시오.</i> """, 'qtext': "<strong>Q16. [원주 계산]</strong><br>반지름의 길이가 5cm인 원의 둘레의 길이를 구하시오. (원주율은 π, 입력시 '파이'로 기재)", 'placeholder': '예: 5파이', 'error': '둘레 계산 오류!', 'ans_check': "ans === '10파이'", 'hint': '반지름이 r인 원의 둘레 공식은 2 * 파이 * r 입니다.'},
    {'qnum': 17, 'title': '원형 뚜껑', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "출구를 안정화해도 렌즈 각도가 어긋나면 무용지물이다. 반지름 9cm, 중심각 120도의 부채꼴 거울 궤도 호의 길이를 구해 렌즈를 조준해라!"<br><br><i>청동 궤도 반사경 튜브가 요란한 기계음과 함께 돌아가며, 부채꼴 호의 길이에 따른 조준 수치를 입력창에 요구합니다.</i> """, 'qtext': '<strong>Q17. [호의 길이 계산]</strong><br>반지름의 길이가 9cm이고 중심각의 크기가 120도인 부채꼴의 호의 길이를 구하시오.', 'placeholder': '예: 3파이', 'error': '금실 길이 부족!', 'ans_check': "ans === '6파이'", 'hint': '반지름이 r, 중심각이 x도인 부채꼴 호의 길이 공식은 2 * 파이 * r * (x / 360) 입니다.'},
    {'qnum': 18, 'title': '수로 조율', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "냉각수 수로 조율이 늦어지면 결국 멜트다운 폭발을 막지 못할 것이다. 부채꼴 모양 수로의 정확한 단면적을 계산해 차단벽을 열어라!"<br><br><i>지하 냉각수 밸브 틈새로 부채꼴 모양의 방열판이 노출됩니다. 반지름 6cm, 중심각 60도 부채꼴 방열 면적 수치를 전송하십시오.</i> """, 'qtext': '<strong>Q18. [부채꼴의 넓이 계산]</strong><br>반지름의 길이가 6cm이고 중심각의 크기가 60도인 부채꼴 모양 홈의 넓이를 구하시오.', 'placeholder': '예: 2파이', 'error': '면적 계산 오류!', 'ans_check': "ans === '6파이'", 'hint': '반지름이 r, 중심각이 x도인 부채꼴 넓이 공식은 파이 * r^2 * (x / 360) 입니다.'},
    {'qnum': 19, 'title': '냉각 밸브', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "마지막 한 걸음인가. 하지만 중심각의 데이터를 소거했다! 중심각 정보 없이 반지름 10cm, 호의 길이 5π cm인 비상 석문의 면적을 계산할 수 있을까!"<br><br><i>게이트 콘솔의 중심각 지시등이 검게 꺼지며 에러를 뿜습니다. 반지름과 호의 길이 데이터만을 활용해 석문 개방 면적 수치를 역도출하십시오.</i> """, 'qtext': '<strong>Q19. [중심각 없이 넓이 구하기]</strong><br>반지름의 길이가 10cm이고 호의 길이가 5π cm인 부채꼴 모양 석문의 넓이를 계산하시오.', 'placeholder': '예: 10파이', 'error': '게이트 수치 오류!', 'ans_check': "ans === '25파이'", 'hint': '반지름 r과 호의 길이 l이 주어졌을 때의 부채꼴 넓이 공식인 (1/2) * r * l 을 활용합니다.'},
    {'qnum': 20, 'title': '최종 마스터 게이트', 'story': """🔮 <strong>[최종 포탈 게이트 락다운 완전 해제]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아누비스-A]</span>: "캡틴! 이제 눈앞의 사막 지상으로 이어지는 마지막 차원 게이트 하나만 남았습니다! 제 마지막 연산 에너지를 동력 셀에 집중하겠습니다! 반지름 8cm 반원 내부에서 4cm 반원 두 개를 뺀 잔여 비대칭 굴절 영역의 면적 상수를 입력해 최종 게이트를 여십시오! 이제 밖으로 탈출할 시간입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[세트-S]</span>: "이럴 수가... 내 핵심 원형 결계 코어가... 완전히 정지당해 소멸한다아앗!" """, 'qtext': '<strong>Q20. [색칠한 부분의 넓이]</strong><br>반지름이 8cm인 반원에서 반지름이 4cm인 반원 두 개를 뺀 색칠된 부분의 넓이를 구하시오.', 'placeholder': '예: 12파이', 'error': '다이얼이 잠겼습니다!', 'ans_check': "ans === '16파이'", 'hint': '반지름 8cm인 큰 반원 넓이에서 반지름 4cm인 작은 반원 두 개(합치면 작은 원 하나)의 넓이를 뺍니다.', "extra_class": "glitch-bg"}
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
            <img src="assets/m1_06_plane_geometry/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">{story}</div>
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
                <div class="story-text" id="outro-dynamic-text">여러분들이 땀을 흘리며 석문에 정답을 입력하고 다이얼을 돌리는 순간! 
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
                        google.script.run.recordEnd(window.userRecordRow, 'm1_06');
                    }
                } catch(e) {
                    console.warn("구글 시트 종료 기록 실패(로컬 테스트 모드):", e);
                }
                
                // 멀티 엔딩 처리
                let outroDiv = document.getElementById("outro-dynamic-text");
                if (outroDiv) {
                    if (totalWrongCount < 5) {
                        outroDiv.innerHTML = `여러분들이 땀을 흘리며 석문에 정답을 입력하고 다이얼을 돌리는 순간! 
                천장에서 쏟아지던 뜨겁고 살인적인 빛줄기가 마지막 거울에 반사되어 지하에 있는 깊은 냉각 수조의 중심부로 정확히 꽂힙니다. 
                쉭-! 하는 굉음과 함께 하얀 수증기가 신전을 가득 채우더니, 이내 굳게 닫혀 있던 탈출용 거대 돌벽이 스르륵 내려앉습니다. 
                눈을 뜰 수 없이 밝은 사막의 태양과 시원한 모래바람이 밀려옵니다. 거울 미궁 탈출에 성공했습니다!`;
                    } else {
                        outroDiv.innerHTML = "탈출 장치가 기동되는 순간! 시스템이 크게 요동칩니다.<br><br>잦은 오답과 연산 지연의 여파로 시스템이 과부하에 걸렸고, 데이터의 일부가 유실되었습니다. 하지만 여러분은 끝까지 포기하지 않고 방화벽을 해제하여 간신히 탈출구로 몸을 피했습니다! 상처투성이의 탈출이었지만, 수학의 지혜로 보물을 획득했습니다. 미션 성공!";
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


# We use regex to replace everything between the start of the first panel and <script> tag
import re
new_content = re.sub(r'<!-- Q1.*?<script>', lambda m: '<!-- Q1 -->\n' + panels_html + '\n        <script>', content, flags=re.DOTALL)

# And for JS:
new_content = re.sub(r'// Q1[\s\S]*?window\.onload = \(\) => \{', lambda m: '// Q1\n' + js_checks + '\n        window.onload = () => {', new_content)

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
new_content = new_content.replace('</style>', glitch_css)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("App 06 updated successfully with regex.")
