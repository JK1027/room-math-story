import os
import re
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
project_root = str(PROJECT_ROOT)
if project_root not in sys.path:
    sys.path.append(project_root)
builders_dir = os.path.join(project_root, "scripts", "builders")
storyboards_dir = os.path.join(project_root, "data", "storyboards")
stories_dir = os.path.join(project_root, "stories")
assets_root = os.path.join(project_root, "apps", "assets")

THEME_METADATA = {
    "m1_01": {"background": "장영실의 조선 공방 자격루실", "artifact": "자격루와 앙부일구의 제어 부품", "player": "조사관", "partner": None, "assistant": "자격(自擊)", "villain": "흑영(黑影)"},
    "m1_02": {"background": "마법 아카데미의 비밀 도서실", "artifact": "고대 마법 그리무어의 핵심 룬", "player": "마법 조사관", "partner": None, "assistant": "그리무어-G", "villain": "섀도우-S"},
    "m1_03": {"background": "스페이스 익스플로러 호 제어실", "artifact": "우주 정거장의 메인 제어 코드", "player": "관제 조사관", "partner": None, "assistant": "오라클-X", "villain": "보이드-V"},
    "m1_04": {"background": "아틀란티스 심해 신전 묘실", "artifact": "고대 아틀란티스의 보석 명판", "player": "캡틴", "partner": "클리오", "assistant": "네레우스", "villain": "포세이돈-V"},
    "m1_05": {"background": "레오나르도 다빈치의 피렌체 비밀 작업실", "artifact": "다빈치의 오르니톱터 설계 도면", "player": "탐사대장", "partner": "필리포", "assistant": "다빈치-메모리", "villain": "코덱스-L"},
    "m1_06": {"background": "이집트 아문-라 태양 신전 거울 미궁", "artifact": "태양 신전의 에너지 거울 반사판", "player": "탐사 요원", "partner": None, "assistant": "아누비스-A", "villain": "세트-S"},
    "m1_07": {"background": "그리스 파르테논 기하학 신전", "artifact": "플라톤 다면체 결정석", "player": "기하 조사관", "partner": None, "assistant": "헤르메스-H", "villain": "모래의 침입자 - 도굴꾼"},
    "m1_08": {"background": "런던 통계국 비밀 기록 보관소", "artifact": "빅벤의 시한폭탄 해체 장부", "player": "보좌 요원", "partner": "왓슨", "assistant": "존 H. 왓슨 - 왓슨", "villain": "범죄의 지배자 - 모리아티"},
    "m2_01": {"background": "연금술사의 비밀 공방", "artifact": "현자의 돌 정제 공식", "player": "연금술 조사관", "partner": None, "assistant": "알케미-H", "villain": "흑마법사-M"},
    "m2_02": {"background": "은하 함대 조종 통제실", "artifact": "블랙홀 탈출 추진 기어 공식", "player": "조사관", "partner": None, "assistant": "기어즈-C", "villain": "바이러스-K"},
    "m2_03": {"background": "황야의 무법자 추적 마차", "artifact": "보안관의 황금 배지 결계", "player": "조사관", "partner": None, "assistant": "실프-F", "villain": "다크-엘프"},
    "m2_04": {"background": "스파이 암호 해독 기지", "artifact": "괴도 X의 보석함 좌표 락다운", "player": "조사관", "partner": None, "assistant": "가드-X", "villain": "괴도-X"},
    "m2_05": {"background": "사이버 월스트리트 네오 서울 터미널", "artifact": "자율주행 택시 메인 제어 콘솔", "player": "조사관", "partner": None, "assistant": "루트-R", "villain": "시스템-에러"},
    "m2_06": {"background": "그리스 아테나 신전", "artifact": "임호텝 사원 파피루스 설계도", "player": "조사관", "partner": None, "assistant": "신전의 수호 정령 - 임호텝", "villain": "사원의 약탈자 - 도굴꾼"},
    "m2_07": {"background": "캡틴 키드의 보물선", "artifact": "거울 게이트 닮음 비례 비약", "player": "조사관", "partner": None, "assistant": "앨리스-Q", "villain": "붉은-여왕"},
    "m2_08": {"background": "라스베이거스 카지노 빌딩", "artifact": "카지노 중앙 서버 확률 보안 락", "player": "조사관", "partner": None, "assistant": "잭팟-D", "villain": "리퍼-R"},
    "m3_01": {"background": "고대 무리수 사원", "artifact": "사원 마스터 록 해제 프리즘", "player": "조사관", "partner": None, "assistant": "피타고라스-P", "villain": "이단자-X"},
    "m3_02": {"background": "현자의 돌 연금술 아카데미", "artifact": "다항식 전개 연금 비약 배합", "player": "조사관", "partner": None, "assistant": "알케미-H", "villain": "흑마법사-M"},
    "m3_03": {"background": "시간의 톱니바퀴 탑", "artifact": "시계탑 비상 피스톤 밸브", "player": "조사관", "partner": None, "assistant": "크로노스-C", "villain": "시간의-방랑자"},
    "m3_04": {"background": "도시 상공 관제탑 레이더 기지", "artifact": "포물선 궤도 안전 정렬 고도", "player": "조사관", "partner": None, "assistant": "이글-E", "villain": "재머-J"},
    "m3_05": {"background": "특이점 중력 우주선", "artifact": "하이퍼드라이브 추진 조향 축", "player": "조사관", "partner": None, "assistant": "아스트로-A", "villain": "블랙홀-B"},
    "m3_06": {"background": "아더 기사단의 원탁 제어실", "artifact": "원형 실드 수선 정합 장치", "player": "조사관", "partner": None, "assistant": "랜슬롯-M", "villain": "모드레드-AI"},
    "m3_07": {"background": "은하 탐사선 데이터 룸", "artifact": "반물질 폭풍 탈출 워프 게이트", "player": "조사관", "partner": None, "assistant": "갤럭시-G", "villain": "안티-매터"},
}

def get_unit_from_filename(filename):
    m2_match = re.search(r'update_app_m2_(\d+)\.py', filename)
    if m2_match:
        return f"m2_{m2_match.group(1).zfill(2)}"
    m3_match = re.search(r'update_app_m3_(\d+)\.py', filename)
    if m3_match:
        return f"m3_{m3_match.group(1).zfill(2)}"
    m1_match = re.search(r'update_app_(\d+)\.py', filename)
    if m1_match:
        return f"m1_{m1_match.group(1).zfill(2)}"
    return None

def parse_builder(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    app_id_match = re.search(r'app_id\s*=\s*["\']([^"\']+)["\']', content)
    app_id = app_id_match.group(1) if app_id_match else ""
    
    qs_match = re.search(r'qs\s*=\s*\[', content)
    if not qs_match:
        return app_id, []
        
    qs_start = qs_match.start()
    bracket_count = 0
    qs_end = -1
    
    start_bracket_idx = content.find('[', qs_start)
    if start_bracket_idx == -1:
        return app_id, []
        
    for i in range(start_bracket_idx, len(content)):
        char = content[i]
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
            if bracket_count == 0:
                qs_end = i + 1
                break
            
    if qs_end == -1:
        return app_id, []
        
    qs_code = content[qs_start:qs_end]
    
    local_vars = {}
    global_vars = {"re": re, "os": os}
    try:
        exec(qs_code, global_vars, local_vars)
        return app_id, local_vars.get("qs", [])
    except Exception as e:
        print(f"Error executing qs code for {os.path.basename(file_path)}: {e}")
        return app_id, []

def detect_characters(qs):
    names = set()
    for q in qs:
        story_text = q.get("story", "")
        found = re.findall(r'\[([^\]]+)\]', story_text)
        for name in found:
            if name not in ["캡틴", "탐사대장", "조사관", "시스템 상태", "선체 상태", "스토리 전개", "시스템 경보", "경보", "일러스트 지시", "일러스트", "자폭 소멸 시퀀스 최종 가동!", "다빈치-메모리 복구율 100% 완전 환수"]:
                clean_name = re.sub(r'<[^>]+>', '', name).strip()
                if clean_name and len(clean_name) < 15:
                    names.add(clean_name)
    return list(names)

def clean_html(text):
    if not text:
        return ""
    text = text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    text = re.sub(r'</?(?:span|strong|i|em|code|strong|b|div|p)(?:\s+[^>]*)*>', '', text)
    text = text.replace("&nbsp;", " ")
    return text.strip()

def get_fallback_theme_name(unit, grade_str):
    # stories/중{학년}/ 아래에서 unit 코드로 시작하는 텍스트 파일명 찾기
    grade_dir = os.path.join(stories_dir, grade_str)
    if os.path.exists(grade_dir):
        for fn in os.listdir(grade_dir):
            if fn.startswith(unit) and fn.endswith(".txt"):
                return fn.replace(".txt", "")
    return f"{unit}_unknown"

def main():
    if not os.path.exists(storyboards_dir):
        os.makedirs(storyboards_dir)
        
    files = sorted(os.listdir(builders_dir))
    
    # 더미 이미지로 복사해 올 원천 PNG 탐색 (가장 용량이 작고 대표적인 것)
    src_png = os.path.join(assets_root, "m1_01_prime_factorization", "intro.png")
    
    for filename in files:
        if not filename.startswith("update_app_") or not filename.endswith(".py"):
            continue
            
        if "update_app_04.py" in filename or "update_app_05.py" in filename:
            print(f"Skipping already customized unit from {filename}")
            continue
            
        unit = get_unit_from_filename(filename)
        if not unit:
            continue
            
        file_path = os.path.join(builders_dir, filename)
        print(f"Processing {filename} ({unit})...")
        
        try:
            from scripts.tools.story.storyboard_parser import load_storyboard_qs
            qs = load_storyboard_qs(unit)
            app_id = unit
        except Exception as e:
            print(f"Error loading storyboard for {unit}: {e}")
            continue
            
        grade_str = "grade1" if "m1_" in unit else ("grade2" if "m2_" in unit else "grade3")
        
        # 에셋 디렉토리 찾기
        assets_folder = None
        for dname in os.listdir(assets_root):
            if dname.startswith(unit) and os.path.isdir(os.path.join(assets_root, dname)):
                assets_folder = dname
                break
                
        # 중3 등 에셋 폴더가 없으면 새로 생성
        if not assets_folder:
            assets_folder = get_fallback_theme_name(unit, grade_str)
            target_assets_dir = os.path.join(assets_root, assets_folder)
            os.makedirs(target_assets_dir, exist_ok=True)
            print(f"  Created empty assets folder: {assets_folder}")
        else:
            target_assets_dir = os.path.join(assets_root, assets_folder)
            
        # 조력자/빌런 감지
        meta = THEME_METADATA.get(unit, {})
        assistant = meta.get("assistant")
        villain = meta.get("villain")
        
        if not assistant or not villain:
            detected_chars = detect_characters(qs)
            fallback_assistant = "조력자-AI"
            fallback_villain = "보안-오토마타"
            
            for char in detected_chars:
                if any(k in char for k in ["코덱스", "포세이돈", "가디언", "가르", "세이렌", "바르토", "드라큘라", "루시퍼", "아누비스", "미노타우로스", "빌런", "메두사", "하데스", "켄타우로스", "키메라", "켈베로스"]):
                    fallback_villain = char
                else:
                    fallback_assistant = char
                    
            if len(detected_chars) >= 2:
                fallback_assistant = detected_chars[0]
                fallback_villain = detected_chars[1]
                for char in detected_chars:
                    if any(k in char for k in ["코덱스", "포세이돈", "가디언", "가르", "세이렌", "바르토", "드라큘라", "루시퍼", "아누비스", "미노타우로스", "빌런", "메두사", "하데스", "켄타우로스", "키메라", "켈베로스"]):
                        fallback_villain = char
                        for other in detected_chars:
                            if other != fallback_villain:
                                fallback_assistant = other
                                break
                        break
            elif len(detected_chars) == 1:
                fallback_assistant = detected_chars[0]
                
            if not assistant:
                assistant = fallback_assistant
            if not villain:
                villain = fallback_villain
            
        theme_title = assets_folder.replace(f"{unit}_", "").replace("_", " ").title()
        
        # 1. 스토리보드 마크다운 생성
        sb_path = os.path.join(storyboards_dir, f"{unit}_storyboard.md")
        
        sb_content = []
        sb_content.append(f"# {grade_str} {int(unit[3:5])}단원 대본집: {theme_title}")
        sb_content.append("\n이 파일은 수학 방탈출 게임의 스토리 대사, 퀴즈 문항, 이벤트 씬 정보를 관리하는 원천 데이터 파일입니다.\n")
        sb_content.append("---")
        sb_content.append("\n# [이미지 매핑]")
        sb_content.append("- intro: intro.png")
        for q in qs:
            qnum = q.get("qnum", q.get("q_num", 1))
            sb_content.append(f"- {qnum}: q{qnum}.png")
        for i in range(1, 5):
            sb_content.append(f"- event{i}: event{i}.png")
        sb_content.append("- outro: outro.png")
        sb_content.append("\n---")
        sb_content.append("\n# [문항 정의]")
        
        for q in qs:
            qnum = q.get("qnum", q.get("q_num", 1))
            title = q.get("title", f"수수께끼 {qnum}")
            story_raw = q.get("story", "")
            qtext = q.get("qtext", q.get("question", ""))
            hint = q.get("hint", "")
            ans_check = q.get("ans_check", f"ans === '{q.get('ans', '')}'")
            placeholder = q.get("placeholder", "정답 입력")
            error = q.get("error", "틀렸습니다. 다시 계산해 보세요.")
            options = q.get("options", [])
            extra_class = q.get("extra_class", "")
            
            sb_content.append(f"\n## Q{qnum}")
            sb_content.append(f"- 제목: {title}")
            sb_content.append(f"- 이미지: ![{title}](../../apps/assets/{assets_folder}/q{qnum}.png)")
            sb_content.append(f"- 질문: {qtext}")
            sb_content.append(f"- 힌트: {hint}")
            sb_content.append(f"- 정답 체크: {ans_check}")
            if options:
                sb_content.append(f"- 선택지: {', '.join(options)}")
            sb_content.append(f"- 플레이스홀더: {placeholder}")
            sb_content.append(f"- 에러 메시지: {error}")
            if extra_class:
                sb_content.append(f"- extra_class: {extra_class}")
            sb_content.append("- 지문:")
            sb_content.append(story_raw)
            
        # 이벤트 정의
        sb_content.append("\n---")
        sb_content.append("\n# [이벤트 정의]")
        
        events_data = [
            {"num": 1, "title": "동력 기어 가동", "progress": 25, "next": "panel_q6", "btn": "계속 전진하기", "story": f"수많은 톱니바퀴 락이 해제되며 동력 기어가 맞물려 돌아가기 시작합니다.\n\n[{assistant}]: \"좋습니다! 1차 결계 동력 충전이 완료되었습니다. 어서 다음 격벽으로 부상하세요!\""},
            {"num": 2, "title": "비상 차단 장치 리셋", "progress": 50, "next": "panel_q11", "btn": "비상 전력 가동", "story": f"코어실의 과열 증기가 멈추며 비상 리셋 시퀀스가 완료됩니다.\n\n[{assistant}]: \"후우... 기지 온도가 하강합니다. 정밀 매니퓰레이터 기어축이 올바르게 락인되었습니다. 다음 3구역으로 돌입합시다!\""},
            {"num": 3, "title": "핵심 복원 제단 활성화", "progress": 75, "next": "panel_q16", "btn": "제단 활성화", "story": f"웅장한 돌벽이 좌우로 나뉘어 회전하며 보석 박힌 복원 제단이 솟구칩니다.\n\n[{assistant}]: \"100% 동기화 성공! 이제 기하학의 모든 비밀이 이 제단에 기입됩니다. 빌런인 {villain}의 최종 마스터 락에 도전하십시오!\""},
            {"num": 4, "title": "탈출 차원 포탈 개방", "progress": 100, "next": "outro", "btn": "지상으로 탈출", "story": f"최종 합동 결계가 붕괴하고 지상으로 향하는 신비로운 황금 동심원 포탈이 소용돌이칩니다.\n\n[{assistant}]: \"탈출 게이트가 열렸습니다! 어서 걸작 설계도를 챙겨 포탈로 도약하십시오!\"\n\n[{villain}]: \"기하학적 무결성을 인정한다... 마스터의 후계자여, 무사 탈출하라.\""}
        ]
        
        for ev in events_data:
            sb_content.append(f"\n## EVENT{ev['num']}")
            sb_content.append(f"- 제목: {ev['title']}")
            sb_content.append(f"- 이미지: ![이벤트{ev['num']}](../../apps/assets/{assets_folder}/event{ev['num']}.png)")
            sb_content.append(f"- 버튼 텍스트: {ev['btn']}")
            sb_content.append(f"- 다음 스테이지: {ev['next']}")
            sb_content.append(f"- 달성도: {ev['progress']}")
            sb_content.append("- 지문:")
            sb_content.append(ev['story'])
            
        with open(sb_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sb_content))
            
        # 2. 대본집(Scenario Script) 생성
        script_path = os.path.join(stories_dir, grade_str, f"{unit}_script.md")
        
        # 테마 메타데이터 추출
        meta = THEME_METADATA.get(unit, {
            "background": "피렌체 지하 밀실",
            "artifact": "다빈치의 오르니톱터 설계 도면",
            "player": "탐사대장",
            "partner": "필리포"
        })
        bg = meta["background"]
        art = meta["artifact"]
        ply = meta["player"]
        ptn = meta["partner"]
        
        partner_desc = f"와 서기 {ptn}" if ptn else ""
        partner_setup = f"\n- **{ptn} (서브 조력자):** {ply}을 보좌하는 기록 서기 겸 조수. 겁이 많으나 기록에 충실함. (인간)" if ptn else ""
        
        sc_content = []
        sc_content.append(f"# {theme_title} 대본집 (Scenario Script) V4: {grade_str} {int(unit[3:5])}단원")
        sc_content.append(f"\n본 대본집은 {grade_str} {int(unit[3:5])}단원 {theme_title} 수학 방탈출 게임의 극적 내러티브를 위해 기획되었습니다.\n")
        sc_content.append("---")
        sc_content.append("\n## 🧭 [기본 캐릭터 설정]")
        sc_content.append(f"- **{ply} (플레이어):** {bg}을 탐색하는 수석 조사관. 기하학/수학 연산 담당.")
        if partner_setup:
            sc_content.append(partner_setup)
        sc_content.append(f"- **{assistant} (메인 조력자):** 탐사대의 기록 복원과 락 해제를 돕는 고대 전송식 오토마타 인격.")
        sc_content.append(f"- **{villain} (메인 빌런):** 기지를 격리하고 자폭을 유도하는 폭주 오토마타 가디언.")
        sc_content.append("- **기아로 (중간 빌런):** 빌런의 핵심 집행 장치이자 강철 수호 장갑 오토마타.")
        
        sc_content.append("\n---")
        sc_content.append("\n## 🎬 [오프닝 & 인트로]")
        sc_content.append("- **기지 상태:** `[배전반 온도: 42°C] [설계 기록 복원율: 15%] [기하학 락 강도: 95%]`")
        sc_content.append("- **스토리 전개:**")
        sc_content.append(f"{bg}에 안착한 {ply}{partner_desc}는 {art}을 회수하기 위해 기동 장치를 돌렸습니다. 그 순간 기지의 모든 격벽 빗장이 내려앉으며 비상 봉인 모드가 기동됩니다. 구체 오토마타인 {villain}의 붉은 광선이 사방을 뒤덮습니다.")
        sc_content.append(f"- **{villain}:** \"삐- 침입자를 소거한다. 40분 뒤 이 기지의 모든 제어 장치를 강제 역회전하여 자폭 격리하겠다! 살아남고 싶다면 수학의 규칙을 증명하라!\"")
        if ptn:
            sc_content.append(f"- **{ptn}:** \"으아악! {ply}님! 또 기계 괴물이 나타나 장벽을 내렸어요! 서판에 적힌 문제를 어서 풀어서 오토마타를 안정시켜야 합니다!\"")
        sc_content.append(f"- **{assistant}:** \"치지직... {ply}님, 제 음성이 전성관관으로 전송되길 바랍니다. {villain}이 마나 펄스 노이즈에 중독되어 폭주하고 있습니다. 20개의 수수께끼를 해독해 봉인을 풀어주세요!\"")
        sc_content.append(f"- **[일러스트 지시 - 0. intro]:** 어두운 석조 기기실 내부에 안착된 복잡한 황동 동력 기어반과 적색 경보 렌즈가 하강하는 인트로 전경.")
        
        sc_content.append("\n---")
        sc_content.append("\n## 🗺️ 제1구역: 탐사의 시작")
        
        for q in qs[:5]:
            qnum = q.get("qnum", q.get("q_num", 1))
            title = q.get("title", "")
            story_clean = clean_html(q.get("story", ""))
            sc_content.append(f"\n### {qnum}) Q{qnum} 해결 전 ({title})")
            sc_content.append(f"- **스토리:** {story_clean}")
            sc_content.append(f"- **[일러스트 지시 - {qnum}. q{qnum}]:** {title} 기하 수치가 새겨진 고대 제단 패널의 상세 뷰.")
            
        sc_content.append("\n---")
        sc_content.append("\n## 🎬 [Event Scene 1: 동력 기어 가동]")
        sc_content.append(f"120도의 동조 신호가 톱니 빗장 기어들을 맞춰 누르자, 회전을 정지하고 벽면 락이 열립니다. 황동 실린더 위로 눈부신 노란색 홀로그램이 피어오릅니다.")
        sc_content.append(f"- **{assistant}:** \"정교한 수학적 균형입니다! {art} 1차가 복원되었습니다. 완벽한 조화의 아름다움입니다.\"")
        if ptn:
            sc_content.append(f"- **{ptn}:** \"{ply}님, 공중에 금빛 홀로그램이 돌고 있어요! 어서 다음 통로로 이동하시죠!\"")
        sc_content.append(f"- **{villain}:** \"감히 마스터의 장치를 열어보는가! 다음 방화벽이 너희를 용융하리라!\"")
        sc_content.append(f"- **[일러스트 지시 - Event 1]:** 둥근 테이블 위로 마나 홀로그램이 서서히 회전하며 자전하는 장면.")
        
        sc_content.append("\n---")
        sc_content.append("\n## 🧭 제 2구역: 교차하는 빛줄기")
        for q in qs[5:10]:
            qnum = q.get("qnum", q.get("q_num", 1))
            title = q.get("title", "")
            story_clean = clean_html(q.get("story", ""))
            sc_content.append(f"\n### {qnum}) Q{qnum} 해결 전 ({title})")
            sc_content.append(f"- **스토리:** {story_clean}")
            sc_content.append(f"- **[일러스트 지시 - {qnum}. q{qnum}]:** {title} 광선 빔이 프리즘 필터 보드와 교차하여 스파크를 일으키는 장면.")
            
        sc_content.append("\n---")
        sc_content.append("\n## 🎬 [Event Scene 2: 비상 차단 장치 리셋]")
        sc_content.append(f"조건과 수식이 맞추어 주입되자, 광선 빔들이 일렬 동축 정렬되어 차단 빗장을 고정합니다. 분출되던 가열 증기가 잦아듭니다.")
        sc_content.append(f"- **{assistant}:** \"자폭 주파수 오버라이드에 성공해 비상 리셋을 완료했습니다. 기지 온도 상승이 멈췄습니다!\"")
        sc_content.append(f"- **기아로:** \"삐- 전력 강제 셧다운. 자폭 시퀀스 유예됨. 빗장을 격리하겠다.\"")
        if ptn:
            sc_content.append(f"- **{ptn}:** \"살았습니다! 청동 장갑 오토마타인 기아로의 안광이 꺼지며 문이 전개되었어요!\"")
        sc_content.append(f"- **[일러스트 지시 - Event 2]:** 푸르스름한 배리어 실드가 터빈을 포근히 둘러싸 안전하게 식혀나가는 긴장 해소 뷰.")
        
        sc_content.append("\n---")
        sc_content.append("\n## 📐 제 3구역: 작도의 방")
        for q in qs[10:15]:
            qnum = q.get("qnum", q.get("q_num", 1))
            title = q.get("title", "")
            story_clean = clean_html(q.get("story", ""))
            sc_content.append(f"\n### {qnum}) Q{qnum} 해결 전 ({title})")
            sc_content.append(f"- **스토리:** {story_clean}")
            sc_content.append(f"- **[일러스트 지시 - {qnum}. q{qnum}]:** {title} 컴퍼스와 가죽 서판, 아날로그 작도판이 결합된 연출.")
            
        sc_content.append("\n---")
        sc_content.append("\n## 🎬 [Event Scene 3: 핵심 복원 제단 활성화]")
        sc_content.append(f"수학적 연산이 완료되자 중앙 코어 유리 돔의 붉은 노이즈가 부서지며 맑고 깨끗한 공기가 실내에 뿜어져 나옵니다.")
        sc_content.append(f"- **{assistant}:** \"시스템 완전 복구율 100%! 이제 빌런 {villain}의 메인 락 제단을 강제로 분리하고 걸작 복원 제단을 기동합니다!\"")
        if ptn:
            sc_content.append(f"- **{ptn}:** \"하아... 공기가 돌아와서 살 것 같습니다! 정면의 기단 석벽들이 무너지며 오색 찬란한 보석 제단이 솟아올라요!\"")
        sc_content.append(f"- **{villain}:** \"최종 마스터 합동 결계를 전개한다! 이 아름다운 유산은 너희의 몫이 아니다!\"")
        sc_content.append(f"- **[일러스트 지시 - Event 3]:** 거대한 황동 기어들이 석조 격벽 틈새로 맞물려 열리고 보라색 마나 광원을 발하는 복합 제단이 솟아오르는 풍경.")
        
        sc_content.append("\n---")
        sc_content.append("\n## ⚙️ 제 4구역: 걸작의 완벽한 복원")
        for q in qs[15:20]:
            qnum = q.get("qnum", q.get("q_num", 1))
            title = q.get("title", "")
            story_clean = clean_html(q.get("story", ""))
            sc_content.append(f"\n### {qnum}) Q{qnum} 해결 전 ({title})")
            sc_content.append(f"- **스토리:** {story_clean}")
            sc_content.append(f"- **[일러스트 지시 - {qnum}. q{qnum}]:** {title} SSS/SAS/ASA 합동 부호가 음각된 피스톤 기둥의 압축 전경.")
            
        sc_content.append("\n---")
        sc_content.append("\n## 🎬 [Event Scene 4: 탈출 차원 포탈 개방]")
        sc_content.append(f"마지막 정답이 해제되며, 기지를 감싸던 적색 장벽선들이 찬란한 오색 입자로 바스러지며 탈출용 차원 포탈로 화합니다.")
        sc_content.append(f"- **{assistant}:** \"탐사 완료! 가방에 복원된 {art}을 챙겨 포탈로 도약하십시오!\"")
        if ptn:
            sc_content.append(f"- **{ptn}:** \"포탈이 황금빛으로 휘몰아쳐요! 빌런이었던 {villain}도 완전히 정화되어 배웅해주네요. 어서 뛰어듭시다!\"")
        sc_content.append(f"- **{villain}:** \"수학 계승 완료. 무결한 지식을 {ply}에게 위임한다. 게이트웨이를 연다.\"")
        sc_content.append(f"- **[일러스트 지시 - Event 4]:** 찬란한 금빛 녹색 차원 링 포탈 정면에서, 머리를 깊이 숙여 배웅하는 백색 렌즈 구체 로봇과 환하게 미소 짓는 조력자의 모습.")
        
        sc_content.append("\n---")
        sc_content.append("\n## 🎬 [엔딩 & 아웃트로]")
        sc_content.append("- **기지 상태:** `[작업실 탈출 성공] [걸작 설계도 100% 획득] [생환 완료]`")
        sc_content.append("- **스토리 전개:**")
        sc_content.append(f"은백색 광채가 선체 조종석과 탐사단을 휘감아 지상으로 쏘아 올립니다. 눈이 멀 만큼 찬란하고 평화로운 하늘 위로 탐사단이 마침내 무사히 부상해 생환을 만끽합니다.")
        if ptn:
            sc_content.append(f"- **{ptn}:** \"살았다! {ply}님, 유산이 안전하게 보존되어 있습니다! 우리가 천재의 기록을 지켰어요!\"")
        sc_content.append(f"- **{assistant}:** \"수학의 이치로 잃어버린 유산을 수호하셨습니다. 당신은 최고의 탐사 대원(조사관)이십니다! 미션 완료!\"")
        sc_content.append(f"- **[일러스트 지시 - outro]:** 맑고 쾌청한 오후 햇살이 비추며 복원된 유산 도면을 안고 귀환하는 {ply}의 실루엣 뷰.")
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sc_content))
            
        # 3. 임시 에셋 이미지 파일 복사 배치 (중3 등 아예 빈 폴더에도 적용)
        if os.path.exists(target_assets_dir):
            base_img = src_png
            
            # 먼저 해당 폴더 내 다른 png 파일이 있나 스캔
            for fn in os.listdir(target_assets_dir):
                if fn.endswith(".png"):
                    base_img = os.path.join(target_assets_dir, fn)
                    break
                    
            # 해당 폴더 내 이미지들을 복사
            for i in range(1, 21):
                t_img = os.path.join(target_assets_dir, f"q{i}.png")
                if not os.path.exists(t_img) and os.path.exists(base_img):
                    shutil.copy2(base_img, t_img)
            
            for name in ["intro.png", "outro.png"]:
                t_img = os.path.join(target_assets_dir, name)
                if not os.path.exists(t_img) and os.path.exists(base_img):
                    shutil.copy2(base_img, t_img)
                    
            for i in range(1, 5):
                t_img = os.path.join(target_assets_dir, f"event{i}.png")
                if not os.path.exists(t_img) and os.path.exists(base_img):
                    shutil.copy2(base_img, t_img)
                    
            print(f"  Completed copy-filling dummy assets for {assets_folder}.")
        else:
            print(f"  Warning: Target asset directory {assets_folder} could not be resolved.")

if __name__ == "__main__":
    main()
