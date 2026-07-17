import os
import re
import shutil
import sys

project_root = r"c:\Coding\Projects\School\room-math-story"
builders_dir = os.path.join(project_root, "scripts", "builders")
storyboards_dir = os.path.join(project_root, "data", "storyboards")
stories_dir = os.path.join(project_root, "stories")
assets_root = os.path.join(project_root, "apps", "assets")

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
        
        app_id, qs = parse_builder(file_path)
        if not qs:
            print(f"Warning: No questions parsed for {filename}")
            continue
            
        grade_str = "중1" if "m1_" in unit else ("중2" if "m2_" in unit else "중3")
        
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
        detected_chars = detect_characters(qs)
        assistant = "조력자-AI"
        villain = "보안-오토마타"
        
        for char in detected_chars:
            if any(k in char for k in ["코덱스", "포세이돈", "가디언", "가르", "세이렌", "바르토", "드라큘라", "루시퍼", "아누비스", "미노타우로스", "빌런", "메두사", "하데스", "켄타우로스", "키메라", "켈베로스"]):
                villain = char
            else:
                assistant = char
                
        if len(detected_chars) >= 2:
            assistant = detected_chars[0]
            villain = detected_chars[1]
            for char in detected_chars:
                if any(k in char for k in ["코덱스", "포세이돈", "가디언", "가르", "세이렌", "바르토", "드라큘라", "루시퍼", "아누비스", "미노타우로스", "빌런", "메두사", "하데스", "켄타우로스", "키메라", "켈베로스"]):
                    villain = char
                    for other in detected_chars:
                        if other != villain:
                            assistant = other
                            break
                    break
        elif len(detected_chars) == 1:
            assistant = detected_chars[0]
            
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
        
        sc_content = []
        sc_content.append(f"# {theme_title} 대본집 (Scenario Script) V4: {grade_str} {int(unit[3:5])}단원")
        sc_content.append(f"\n본 대본집은 {grade_str} {int(unit[3:5])}단원 {theme_title} 수학 방탈출 게임의 극적 내러티브를 위해 기획되었습니다.\n")
        sc_content.append("---")
        sc_content.append("\n## 🧭 [기본 캐릭터 설정]")
        sc_content.append("- **탐사대장 (플레이어):** 유실된 지식의 방을 탐색하는 수석 조사관. 기하학/수학 연산 담당.")
        sc_content.append("- **필리포 (서브 조력자):** 탐사대장을 보좌하는 기록 서기 겸 조수. 겁이 많으나 기록에 충실함. (인간)")
        sc_content.append(f"- **{assistant} (메인 조력자):** 탐사대의 기록 복원과 락 해제를 돕는 고대 전송식 오토마타 인격.")
        sc_content.append(f"- **{villain} (메인 빌런):** 기지를 격리하고 자폭을 유도하는 폭주 오토마타 가디언.")
        sc_content.append("- **기아로 (중간 빌런):** 빌런의 핵심 집행 장치이자 강철 수호 장갑 오토마타.")
        
        sc_content.append("\n---")
        sc_content.append("\n## 🎬 [오프닝 & 인트로]")
        sc_content.append("- **기지 상태:** `[배전반 온도: 42°C] [설계 기록 복원율: 15%] [기하학 락 강도: 95%]`")
        sc_content.append("- **스토리 전개:**")
        sc_content.append(f"피렌체 지하 밀실에 안착한 탐사대장과 서기 필리포는 다빈치의 잃어버린 도면을 회수하기 위해 기동 장치를 돌렸습니다. 그 순간 기지의 모든 격벽 빗장이 내려앉으며 비상 봉인 모드가 기동됩니다. 구체 오토마타인 {villain}의 붉은 광선이 사방을 뒤덮습니다.")
        sc_content.append(f"- **{villain}:** \"삐- 침입자를 소거한다. 40분 뒤 이 밀실의 모든 기어 축을 강제 역회전하여 자폭 매립하겠다! 살아남고 싶다면 기하학 규칙을 증명하라!\"")
        sc_content.append(f"- **필리포:** \"으아악! 대장님! 또 기계 괴물이 나타나 장벽을 내렸어요! 서판에 적힌 공식을 어서 풀어서 오토마타를 안정시켜야 합니다!\"")
        sc_content.append(f"- **{assistant}:** \"치지직... 탐사대장님, 제 음성이 전성관관으로 전송되길 바랍니다. {villain}이 마나 펄스 노이즈에 중독되어 폭주하고 있습니다. 20개의 기하학 수수께끼를 해독해 봉인을 풀어주세요!\"")
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
        sc_content.append(f"120도의 동조 신호가 톱니 빗장 기어들을 맞춰 누르자, 회전을 정지하고 벽면 락이 열립니다. 황동 실린더 위로 눈부신 노란색 기하 홀로그램이 피어오릅니다.")
        sc_content.append(f"- **{assistant}:** \"정교한 기하 균형입니다! 마스터 다빈치의 비행선 도판 1차가 복원되었습니다. 점과 선이 완벽히 면을 이룬 조화의 아름다움입니다.\"")
        sc_content.append(f"- **필리포:** \"대장님, 공중에 금빛 홀로그램이 돌고 있어요! 어서 다음 나선 계단 아래의 통로로 내려가시죠!\"")
        sc_content.append(f"- **{villain}:** \"감히 마스터의 기하 코덱스를 훔쳐보려 하는가! 다음 광선 방막이 너희를 용융하리라!\"")
        sc_content.append(f"- **[일러스트 지시 - Event 1]:** 둥근 구리 테이블 위로 금빛 마나 오르니톱터 도면이 서서히 회전하며 자전하는 장면.")
        
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
        sc_content.append(f"평행 조건과 엇각이 맞추어 주입되자, 광선 빔들이 일렬 동축 정렬되어 차단 빗장을 고정합니다. 분출되던 가열 증기가 잦아듭니다.")
        sc_content.append(f"- **{assistant}:** \"자폭 주파수 오버라이드에 성공해 비상 리셋을 완료했습니다. 기지 온도 상승이 멈췄습니다!\"")
        sc_content.append(f"- **기아로:** \"삐- 전력 강제 셧다운. 자폭 시퀀스 유예됨. 빗장을 격리하겠다.\"")
        sc_content.append(f"- **필리포:** \"살았습니다! 청동 장갑 오토마타인 기아로의 안광이 꺼지며 문이 전개되었어요!\"")
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
        sc_content.append(f"삼각형의 최종 작도가 완료되자 중앙 코어 유리 돔의 붉은 노이즈가 부서지며 맑고 깨끗한 공기가 실내에 뿜어져 나옵니다.")
        sc_content.append(f"- **{assistant}:** \"시스템 완전 복구율 100%! 이제 빌런 {villain}의 메인 락 제단을 강제로 분리하고 걸작 복원 제단을 기동합니다!\"")
        sc_content.append(f"- **필리포:** \"하아... 공기가 돌아와서 살 것 같습니다! 정면의 기단 석벽들이 무너지며 오색 찬란한 보석 제단이 솟아올라요!\"")
        sc_content.append(f"- **{villain}:** \"최종 마스터 합동 결계를 전개한다! 이 아름다운 복원도는 침입자의 몫이 아니다!\"")
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
        sc_content.append(f"직각삼각형의 마지막 합동이 해제되며, 기지를 감싸던 적색 장벽선들이 찬란한 에메랄드색 오색 입자로 바스러지며 탈출용 차원 포탈로 화합니다.")
        sc_content.append(f"- **{assistant}:** \"탐사 완료! 가방에 복원된 마스터의 오르니톱터 도면을 챙겨 포탈로 도약하십시오!\"")
        sc_content.append(f"- **필리포:** \"포탈이 황금빛으로 휘몰아쳐요! 빌런이었던 {villain}도 완전히 정화되어 배웅해주네요. 어서 뛰어듭시다!\"")
        sc_content.append(f"- **{villain}:** \"기하 계승 완료. 무결한 지식을 탐사대장에게 위임한다. 게이트웨이를 연다.\"")
        sc_content.append(f"- **[일러스트 지시 - Event 4]:** 찬란한 금빛 녹색 차원 링 포탈 정면에서, 머리를 깊이 숙여 배웅하는 백색 렌즈 구체 로봇 코덱스-L과 환하게 미소 짓는 조력자의 모습.")
        
        sc_content.append("\n---")
        sc_content.append("\n## 🎬 [엔딩 & 아웃트로]")
        sc_content.append("- **기지 상태:** `[작업실 탈출 성공] [걸작 설계도 100% 획득] [생환 완료]`")
        sc_content.append("- **스토리 전개:**")
        sc_content.append("은백색 광채가 선체 조종석과 탐사단을 휘감아 지상으로 쏘아 올립니다. 눈이 멀 만큼 찬란하고 평화로운 피렌체 광장의 맑은 하늘 위로 탐사단이 마침내 무사히 부상해 생환을 만끽합니다.")
        sc_content.append(f"- **필리포:** \"살았다! 진짜 피렌체의 푸른 하늘이에요! 캡틴, 도면이 가방에 안전하게 보존되어 있습니다! 우리가 천재의 기록을 지켰어요!\"")
        sc_content.append(f"- **{assistant}:** \"(음성 전성관관관관으로) 기하의 이치로 천재 다빈치의 잃어버린 유산을 수호하셨습니다. 당신은 진정 최고의 기하 탐사 대장이십니다! 미션 완료!\"")
        sc_content.append(f"- **[일러스트 지시 - outro]:** 맑고 쾌청한 오후 햇살이 대리석 피렌체 아치 아치를 비추며 복원된 유산 도면을 안고 귀환하는 탐사대장의 실루엣 뷰.")
        
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
