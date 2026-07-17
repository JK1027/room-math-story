import os
import re
from pathlib import Path

# --- Central Configs Loading ---
import sys
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(os.path.dirname(_cur)))
if _root not in sys.path:
    sys.path.append(_root)
from scripts.config import paths
from scripts.config.constants import SUPPORTED_GRADES

storyboards_root = str(paths.STORYBOARDS_DIR)
archive_dir = str(paths.ARCHIVE_DIR / "releases")

# 초정밀 캐릭터 매핑 테이블
unit_characters = {
    "m1_01": {"assistant": "자격(自擊)", "villain": "흑영(黑影)"},
    "m1_02": {"assistant": "그리무어-G", "villain": "폭주 마법인격"},
    "m1_03": {"assistant": "오라클-X", "villain": "바이러스-V"},
    "m1_04": {"assistant": "네레우스", "villain": "포세이돈-V"},
    "m1_05": {"assistant": "필리포", "villain": "기아로"},
    "m1_06": {"assistant": "가디언-M", "villain": "아누비스-A"},
    "m1_07": {"assistant": "테세우스", "villain": "미노타우로스"},
    "m1_08": {"assistant": "코덱스-L", "villain": "모리아티"},
    "m2_01": {"assistant": "기아로", "villain": "바르토"},
    "m2_02": {"assistant": "엘론", "villain": "루시퍼"},
    "m2_03": {"assistant": "시드", "villain": "가르-V"},
    "m2_04": {"assistant": "호루스", "villain": "세트"},
    "m2_05": {"assistant": "아리아드네", "villain": "미노타우로스"},
    "m2_06": {"assistant": "아틀란", "villain": "크라켄"},
    "m2_07": {"assistant": "헤라클레스", "villain": "하이드라"},
    "m2_08": {"assistant": "크로노스", "villain": "네메시스"},
    "m3_01": {"assistant": "임호텝", "villain": "소베크"},
    "m3_02": {"assistant": "반 헬싱", "villain": "드라큘라"},
    "m3_03": {"assistant": "솔로몬", "villain": "아스모데우스"},
    "m3_04": {"assistant": "데카르트", "villain": "메피스토"},
    "m3_05": {"assistant": "피타고라스", "villain": "히파소스"},
    "m3_06": {"assistant": "유클리드", "villain": "프로클로스"},
    "m3_07": {"assistant": "가우스", "villain": "크로네커"}
}

def get_unit_from_path(filepath):
    filename = os.path.basename(filepath)
    match = re.search(r'(m\d+_\d+)', filename)
    return match.group(1) if match else None

def get_theme_category(unit):
    if unit in ["m1_01"]:
        return "조선"
    elif unit in ["m1_02", "m2_02", "m2_08", "m3_03", "m3_05", "m3_06"]:
        return "마법"
    elif unit in ["m1_03"]:
        return "SF"
    elif unit in ["m1_04", "m2_06", "m2_07"]:
        return "그리스"
    elif unit in ["m1_06", "m2_04", "m3_01"]:
        return "이집트"
    elif unit in ["m1_07", "m3_04", "m3_07"]:
        return "그리스"
    elif unit in ["m1_08"]:
        return "셜록"
    elif unit in ["m2_01", "m2_03", "m2_05"]:
        return "스팀펑크"
    elif unit in ["m3_02"]:
        return "뱀파이어"
    return "기본"

def generate_theme_events(unit, theme, assistant, villain):
    if theme == "조선":
        return [
            {"num": 1, "title": "청동 물레방아 수류 가동", "progress": 25, "next": "panel_q6", "btn": "계속 전진하기", 
             "story": f"수력 제어판의 기역 빗장이 해제되며 웅장한 청동 물레방아가 급류와 함께 힘차게 회전하기 시작합니다.\n\n[{assistant}]: \"좋습니다! 1차 수류 동력이 자격루의 수위관으로 충전되었습니다. 어서 다음 격실로 올라가십시오!\""},
            {"num": 2, "title": "수은 압력 밸브 비상 리셋", "progress": 50, "next": "panel_q11", "btn": "비상 전력 가동", 
             "story": f"끓어오르던 은빛 수은 배출 파이프의 과열 밸브 압력이 낮아지며 비상 제어 시퀀스가 완료됩니다.\n\n[{assistant}]: \"후우... 배출 압력이 진정되었습니다. 중앙 가동 기어축이 올바르게 락인되었습니다. 다음 3구역으로 돌입합시다!\""},
            {"num": 3, "title": "조선식 기단 비밀 함 열기", "progress": 75, "next": "panel_q16", "btn": "제단 활성화", 
             "story": f"벽면의 웅장한 돌벽들이 무너지며 은백색 기단 위에 비밀 청동 함이 천천히 솟구쳐 오릅니다.\n\n[{assistant}]: \"100% 동기화 성공! 이제 앙부일구 영침의 모든 비밀 기하 수치가 기입됩니다. 빌런인 {villain}의 최종 마스터 락에 도전하십시오!\""},
            {"num": 4, "title": "앙부일구 영침 봉인 해제", "progress": 100, "next": "outro", "btn": "공방 밖으로 탈출", 
             "story": f"최종 결계 살기가 걷히며 앙부일구의 영침 틈새로 찬란한 황금빛 출구 포탈이 소용돌이칩니다.\n\n[{assistant}]: \"공방 문이 열렸습니다! 어서 장영실 마스터의 복원 설계도를 챙겨 탈출하십시오!\"\n\n[{villain}]: \"조선의 기하학적 시간 질서를 인정한다... 무사 탈출하라.\""}
        ]
    elif theme == "마법":
        return [
            {"num": 1, "title": "마나 빗장 해제", "progress": 25, "next": "panel_q6", "btn": "계속 전진하기", 
             "story": f"크리스탈 제단의 마나 빗장이 해제되며 영롱한 오색 보석들이 회전하며 빛의 공명을 시작합니다.\n\n[{assistant}]: \"좋습니다! 1차 마나 마법 장벽이 해제되었습니다. 어서 서고의 다음 격실로 전진하십시오!\""},
            {"num": 2, "title": "폭주 마나 핵 비상 리셋", "progress": 50, "next": "panel_q11", "btn": "비상 전력 가동", 
             "story": f"과열되던 마법 봉인 핵의 붉은 열기가 식어 내리며 안정적인 마법 비상 제어가 완료됩니다.\n\n[{assistant}]: \"후우... 마나 안정도가 복구되었습니다. 정밀 마나 레일 락이 해제되었습니다. 다음 3구역으로 돌입합시다!\""},
            {"num": 3, "title": "고대 대마법사 제단 기동", "progress": 75, "next": "panel_q16", "btn": "제단 활성화", 
             "story": f"서고 중앙의 대리석 석조들이 돌며 보라색 마나를 발산하는 고대 마법 제단이 솟아오릅니다.\n\n[{assistant}]: \"100% 동기화 성공! 이제 마법 기하학의 모든 비밀이 기입됩니다. 빌런인 {villain}의 최종 마스터 락에 도전하십시오!\""},
            {"num": 4, "title": "성간 차원 마법 포탈 개방", "progress": 100, "next": "outro", "btn": "지상으로 탈출", 
             "story": f"최종 이중 봉인이 파괴되며 은하수가 흐르는 영롱한 파란빛 차원 워프 포탈이 소용돌이칩니다.\n\n[{assistant}]: \"탈출 게이트가 열렸습니다! 어서 고대 현자의 유산 양가죽 고서를 챙겨 도약하십시오!\"\n\n[{villain}]: \"마법의 무결성을 인정하노라... 후계자여, 무사히 탈출하여라.\""}
        ]
    elif theme == "이집트":
        return [
            {"num": 1, "title": "파피루스 석벽 빗장 해제", "progress": 25, "next": "panel_q6", "btn": "계속 전진하기", 
             "story": f"웅장한 돌벽 속 기어 빗장이 해제되며 이집트 기하 기호들이 태양빛과 함께 가동됩니다.\n\n[{assistant}]: \"좋습니다! 1차 피라미드 석문 장벽이 해제되었습니다. 어서 다음 통로로 이동하십시오!\""},
            {"num": 2, "title": "함정 독가스 유입 비상 리셋", "progress": 50, "next": "panel_q11", "btn": "비상 전력 가동", 
             "story": f"밀실에 뿜어져 나오던 가열된 황사 가스 유입이 차단되며 비상 통풍구가 개방 리셋됩니다.\n\n[{assistant}]: \"후우... 함정 온도와 가스가 안정되었습니다. 정밀 차단문 락이 해제되었습니다. 다음 3구역으로 돌입합시다!\""},
            {"num": 3, "title": "파라오 복원 제단 활성화", "progress": 75, "next": "panel_q16", "btn": "제단 활성화", 
             "story": f"모래벽이 갈라져 내리며 황금 보석이 아로새겨진 거대한 사막의 복원 제단이 솟구쳐 오릅니다.\n\n[{assistant}]: \"100% 동기화 성공! 이제 고대 이집트의 모든 건축 기하 비밀이 복원됩니다. 빌런인 {villain}의 최종 마스터 락에 도전하십시오!\""},
            {"num": 4, "title": "태양신 라의 광선 탈출구 개방", "progress": 100, "next": "outro", "btn": "지상으로 탈출", 
             "story": f"최종 죽음의 봉인이 부서지고 지상으로 향하는 눈부신 황금빛 게이트웨이가 소용돌이칩니다.\n\n[{assistant}]: \"탈출 해치가 열렸습니다! 어서 고대 파피루스 설계도를 품고 도약하십시오!\"\n\n[{villain}]: \"이집트의 기하학적 완벽함을 확인했다... 대장에게 설계도를 위임한다.\""}
        ]
    elif theme == "그리스":
        return [
            {"num": 1, "title": "대리석 회전 기단 기동", "progress": 25, "next": "panel_q6", "btn": "계속 전진하기", 
             "story": f"신전의 대리석 기둥 기어 빗장이 어긋나 맞춰 돌며 대리석 회전 통로가 개방되기 시작합니다.\n\n[{assistant}]: \"좋습니다! 1차 신전 지하 석문이 정렬되었습니다. 어서 다음 원통 격벽으로 진입하십시오!\""},
            {"num": 2, "title": "유리 구체 수압 비상 리셋", "progress": 50, "next": "panel_q11", "btn": "비상 전력 가동", 
             "story": f"지하 수압 터빈의 밸브가 복구되며 비상 배수가 리셋 가동됩니다.\n\n[{assistant}]: \"후우... 신전 수온과 압력이 내려갑니다. 회전체 동축 락이 올바르게 고정되었습니다. 다음 3구역으로 전진하십시오!\""},
            {"num": 3, "title": "플라톤 다면체 결정석 제단 활성화", "progress": 75, "next": "panel_q16", "btn": "제단 활성화", 
             "story": f"거대한 조각상 돌벽이 갈라지며 오색으로 회전하며 반짝이는 다면체 보석 결정석 제단이 솟아오릅니다.\n\n[{assistant}]: \"100% 동기화 성공! 이제 기하학의 모든 신성 기하 공식이 기입됩니다. 빌런인 {villain}의 최종 마스터 락에 도전하십시오!\""},
            {"num": 4, "title": "아르키메데스의 유리 구체 포탈 개방", "progress": 100, "next": "outro", "btn": "지상으로 탈출", 
             "story": f"최종 석화 결계가 부서지고 그리스 지상으로 연결되는 에메랄드색 오색 차원 링 포탈이 소용돌이칩니다.\n\n[{assistant}]: \"탈출 게이트가 개방되었습니다! 어서 결정 서판 유산을 챙겨 뛰어듭니다!\"\n\n[{villain}]: \"입체의 무결성을 인정하노라... 무사 탈출하라.\""}
        ]
    elif theme == "셜록":
        return [
            {"num": 1, "title": "증기압 터빈 태엽 가동", "progress": 25, "next": "panel_q6", "btn": "계속 전진하기", 
             "story": f"구리 배관 밸브가 풀리며 차가운 런던의 지기실 증기 터빈이 힘찬 소리를 내며 작동하기 시작합니다.\n\n[{assistant}]: \"좋습니다! 1차 배기 밸브의 압력이 복구되었습니다. 다음 2구역의 보일러실로 진입합시다!\""},
            {"num": 2, "title": "석탄 보일러 압력 비상 리셋", "progress": 50, "next": "panel_q11", "btn": "비상 전력 가동", 
             "story": f"과열 경보가 울리던 석탄 밸브가 차단되며 보일러실 온도가 하강 안전 리셋됩니다.\n\n[{assistant}]: \"후우... 증기 배전반 압력이 하강합니다. 정밀 톱니바퀴 락이 올바르게 락인되었습니다. 다음 3구역으로 돌입합시다!\""},
            {"num": 3, "title": "비밀 기하 금고 활성화", "progress": 75, "next": "panel_q16", "btn": "제단 활성화", 
             "story": f"벽면의 웅장한 가죽 장식 격판들이 양좌로 분리되며 보석이 수놓아진 비밀 금고 기단이 솟아오릅니다.\n\n[{assistant}]: \"100% 동기화 성공! 이제 셜록 런던 기지의 최종 데이터 디바이스가 락 해제되었습니다. 빌런 {villain}의 최종 마스터 락에 도전하십시오!\""},
            {"num": 4, "title": "런던 베이커가 탈출 도어 개방", "progress": 100, "next": "outro", "btn": "지상으로 탈출", 
             "story": f"최종 악성 해킹 방어벽이 무력화되고, 지상 런던 베이커가로 향하는 비밀 금속 포탈이 찬란하게 가동됩니다.\n\n[{assistant}]: \"탈출 게이트가 열렸습니다! 어서 셜록의 비밀 유산 설계 서판을 가방에 담아 탈출합시다!\"\n\n[{villain}]: \"추리와 기하학적 논리를 인정한다... 안전한 귀환을 승인하겠다.\""}
        ]
    elif theme == "스팀펑크":
        return [
            {"num": 1, "title": "구리 태엽 구동기 충전", "progress": 25, "next": "panel_q6", "btn": "계속 전진하기", 
             "story": f"수십 개의 황동 구리 태엽 락이 해제되며 톱니바퀴 동력 기어가 힘차게 급가속 가동을 시작합니다.\n\n[{assistant}]: \"좋습니다! 1차 유압 동력 충전이 완료되었습니다. 어서 다음 격벽 터빈실로 돌입하세요!\""},
            {"num": 2, "title": "증기 파이프 과열 비상 리셋", "progress": 50, "next": "panel_q11", "btn": "비상 전력 가동", 
             "story": f"과열 배기 밸브가 기계식으로 리셋 해제되며 스팀 터빈의 과열 증기가 멈춰 가라앉습니다.\n\n[{assistant}]: \"후우... 공장 온도가 급격히 하강합니다. 정밀 매니퓰레이터 기어축이 락인되었습니다. 다음 3구역으로 돌입합시다!\""},
            {"num": 3, "title": "스팀펑크 메인 코어 제단 전개", "progress": 75, "next": "panel_q16", "btn": "제단 활성화", 
             "story": f"중앙 유압 패널이 좌우로 나뉘며 오색 마나 불꽃을 내뿜는 피스톤 동력 제단이 활성화됩니다.\n\n[{assistant}]: \"100% 동기화 성공! 스팀펑크 기하 설계의 모든 비밀이 기입됩니다. 빌런인 {villain}의 최종 마스터 락에 도전하십시오!\""},
            {"num": 4, "title": "공장 탈출 차원 포탈 개방", "progress": 100, "next": "outro", "btn": "지상으로 탈출", 
             "story": f"최종 강철 빗장이 풀리고 공장 밖 지상으로 향하는 에메랄드색 황금 링 포탈이 요동치며 작동합니다.\n\n[{assistant}]: \"탈출 해치가 열렸습니다! 어서 복원 코덱스 서판을 챙겨 포탈로 점프하십시오!\"\n\n[{villain}]: \"유압 기하학의 무결성을 인정하마... 무사 탈출하라.\""}
        ]
    elif theme == "뱀파이어":
        return [
            {"num": 1, "title": "어둠의 뱀파이어 관 빗장 해제", "progress": 25, "next": "panel_q6", "btn": "계속 전진하기", 
             "story": f"뱀파이어 관 석문 빗장이 해제되며 붉은색 기하 보석들이 어둠 속에서 자전하며 빛을 발합니다.\n\n[{assistant}]: \"좋습니다! 1차 뱀파이어 방벽이 열렸습니다. 어서 성의 다음 깊숙한 탑으로 올라가십시오!\""},
            {"num": 2, "title": "성 지하 멜트다운 밸브 비상 리셋", "progress": 50, "next": "panel_q11", "btn": "비상 전력 가동", 
             "story": f"지하 용광로 배출기가 멈춰 식어 내리며 비상 제어 시스템이 리셋 완료됩니다.\n\n[{assistant}]: \"후우... 어둠의 온도가 하강합니다. 정밀 톱니바퀴 레일이 올바르게 락인되었습니다. 다음 3구역으로 돌입합시다!\""},
            {"num": 3, "title": "드라큘라 복원 비밀 제단 활성화", "progress": 75, "next": "panel_q16", "btn": "제단 활성화", 
             "story": f"석조 박쥐 문양 벽이 회전해 열리며 찬란하게 회전하는 드라큘라의 복원 제단이 솟아오릅니다.\n\n[{assistant}]: \"100% 동기화 성공! 기하 십자가의 비밀이 이 제단에 새겨집니다. 빌런인 {villain}의 최종 마스터 락에 도전하십시오!\""},
            {"num": 4, "title": "달빛 탈출 차원 통로 개방", "progress": 100, "next": "outro", "btn": "지상으로 탈출", 
             "story": f"최종 어둠의 결계가 무력화되고, 밤하늘 달빛이 쏟아지는 성 외곽으로 통하는 은빛 워프 포탈이 가동됩니다.\n\n[{assistant}]: \"탈출 게이트가 열렸습니다! 어서 뱀파이어의 유산 보석 서판을 챙겨 포탈로 탈출하십시오!\"\n\n[{villain}]: \"어둠의 기하 논리를 인정한다... 성 밖으로 무사히 빠져나가라.\""}
        ]
    # Fallback
    return [
        {"num": 1, "title": "동력 보조 장치 충전", "progress": 25, "next": "panel_q6", "btn": "계속 전진하기", 
         "story": f"제어 회로 기어 빗장이 해제되며 예비 백업 전력이 동력 장치로 가속 가동을 시작합니다.\n\n[{assistant}]: \"좋습니다! 1차 결계 동력 충전이 완료되었습니다. 어서 다음 격실로 전진하십시오!\""},
        {"num": 2, "title": "과열 배출 터빈 비상 리셋", "progress": 50, "next": "panel_q11", "btn": "비상 전력 가동", 
         "story": f"과열 배기 터빈의 고열 경고음이 멈추며 비상 리셋 시퀀스가 완료됩니다.\n\n[{assistant}]: \"후우... 기지 온도가 가라앉습니다. 정밀 매니퓰레이터 기어축이 올바르게 고정되었습니다. 다음 3구역으로 돌입합시다!\""},
        {"num": 3, "title": "중앙 코어 복원 제단 활성화", "progress": 75, "next": "panel_q16", "btn": "제단 활성화", 
         "story": f"차폐 돌벽이 나뉘며 오색 마나를 뿜어내는 수려한 중앙 서버 복원 제단이 솟구쳐 활성화됩니다.\n\n[{assistant}]: \"100% 동기화 성공! 기하 코덱스의 모든 비밀이 이 제단에 기입됩니다. 빌런인 {villain}의 최종 마스터 락에 도전하십시오!\""},
        {"num": 4, "title": "탈출 게이트웨이 포탈 개방", "progress": 100, "next": "outro", "btn": "지상으로 탈출", 
         "story": f"최종 마스터 락다운 프로토콜이 해제되고 지상으로 향하는 신비로운 탈출 차원 포탈이 개방됩니다.\n\n[{assistant}]: \"탈출 해치가 열렸습니다! 어서 데이터 서판 유산을 챙겨 포탈로 도약하십시오!\"\n\n[{villain}]: \"무결한 수학적 지식을 인정한다... 무사 탈출하라.\""}
    ]

def patch_file_events(filepath, unit, theme, assistant, villain):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    events = generate_theme_events(unit, theme, assistant, villain)
    
    # 1. ## EVENT1 ~ EVENT4 정규식 치환
    for ev in events:
        ev_regex = r'(## EVENT' + str(ev["num"]) + r'\n- 제목:[^\n]*\n- 이미지:[^\n]*\n- [^\n]*\n- [^\n]*\n- 달성도:[^\n]*\n- 지문:\n)([\s\S]*?)(?=\n## EVENT|\n# \[이벤트 정의\]|\n---|\n# \[|$)'
        def replace_event(match):
            header = match.group(1)
            return header + ev["story"] + "\n"
        content = re.sub(ev_regex, replace_event, content)
        
    # 2. 대본집 포맷의 교체 (stories/archive/ 내에 script.md 파일이 있을 경우)
    for ev in events:
        sc_regex = r'(## 🎬 \[Event Scene ' + str(ev["num"]) + r':[^\n]*\]\n)([\s\S]*?)(?=\n## 🧭|\n## ⚙️|\n## 🎬 \[Event Scene|\n## 🎬 \[엔딩|\n---|\n# \[|$)'
        
        if ev["num"] == 1:
            sc_story = f"{ev['story']}\n- **[일러스트 지시 - Event 1]:** 1차 활성화 패널 콘솔 뷰."
        elif ev["num"] == 2:
            sc_story = f"{ev['story']}\n- **[일러스트 지시 - Event 2]:** 냉각 장치 또는 리셋 시퀀스 비주얼."
        elif ev["num"] == 3:
            sc_story = f"{ev['story']}\n- **[일러스트 지시 - Event 3]:** 중앙 복원 제단 전개 뷰."
        else:
            sc_story = f"{ev['story']}\n- **[일러스트 지시 - Event 4]:** 포탈 게이트 개방 및 배웅하는 조력자의 뷰."
            
        def replace_sc_event(match):
            header = match.group(1)
            return header + sc_story + "\n"
        content = re.sub(sc_regex, replace_sc_event, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    for grade in SUPPORTED_GRADES:
        grade_dir = str(paths.storyboard_dir(grade))
        if not os.path.exists(grade_dir):
            continue
            
        for filename in os.listdir(grade_dir):
            if not filename.endswith("_storyboard.md"):
                continue
                
            unit = get_unit_from_path(filename)
            if not unit:
                continue
                
            if unit in ["m1_03", "m1_04", "m1_05"]:
                print(f"Skipping customized storyboard: {filename}")
                continue
                
            filepath = os.path.join(grade_dir, filename)
            
            # 사전 정의된 정확한 캐릭터 맵 정보 참조
            char_info = unit_characters.get(unit, {"assistant": "조력자-AI", "villain": "보안-오토마타"})
            assistant = char_info["assistant"]
            villain = char_info["villain"]
            
            theme = get_theme_category(unit)
            print(f"Patching {filename} ({unit}) -> Theme: {theme}, Assistant: {assistant}, Villain: {villain}")
            
            # 스토리보드 치환
            patch_file_events(filepath, unit, theme, assistant, villain)
            
            # 대본집 치환
            script_filename = f"{unit}_script.md"
            if unit == "m1_04":
                script_filename = "m1_04_atlantis_script.md"
            elif unit == "m1_05":
                script_filename = "m1_05_geometry_script.md"
                
            script_path = os.path.join(archive_dir, script_filename)
            if os.path.exists(script_path):
                print(f"  Patching corresponding script: {script_filename}")
                patch_file_events(script_path, unit, theme, assistant, villain)

if __name__ == "__main__":
    main()
