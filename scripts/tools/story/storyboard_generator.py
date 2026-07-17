import os
import re
import shutil
import sys
import yaml
from pathlib import Path

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(os.path.dirname(_cur)))
if _root not in sys.path:
    sys.path.append(_root)
from scripts.config import paths

PROJECT_ROOT = paths.ROOT_DIR
stories_dir = str(paths.STORIES_DIR)
apps_assets_root = str(paths.APPS_DIR / "assets")
game_data_root = str(PROJECT_ROOT / "game_data")

# 허용되는 YAML 스키마 필드 (안전 장치)
ALLOWED_YAML_FIELDS = {"image_mapping", "questions", "events"}

def parse_script_md(filepath):
    """
    script.md 파일을 읽어 오프닝, 엔딩, Q1~Q20의 지문, Event Scene 1~4의 지문을 파싱합니다.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')

    # 1. 인트로 파싱
    intro_match = re.search(r'## 🎬 \[오프닝 & 인트로\]\n([\s\S]*?)(?:\n---|\n## |$)', content)
    intro_story = intro_match.group(1).strip() if intro_match else ""

    # 2. 아웃트로 파싱
    outro_match = re.search(r'## 🎬 \[엔딩 & 아웃트로\]\n([\s\S]*?)(?:\n---|\n## |$)', content)
    outro_story = outro_match.group(1).strip() if outro_match else ""

    # 3. 문제 Q1 ~ Q20 파싱
    qs_stories = {}
    q_matches = re.finditer(r'###\s*(\d+)\)\s*Q\d+\s*해결\s*전\s*\([^\)]*\)\n([\s\S]*?)(?=\n###|\n##|\n---|$)', content)
    for m in q_matches:
        qnum = int(m.group(1))
        body = m.group(2).strip()
        
        # - 스토리: ... 라인 찾아서 추출
        story_match = re.search(r'-\s*(?:\*\*스토리\*\*|스토리)\s*:\s*([\s\S]*)', body)
        if story_match:
            qs_stories[qnum] = story_match.group(1).strip()
        else:
            qs_stories[qnum] = body

    # 4. Event Scene 1 ~ 4 파싱
    events_stories = {}
    ev_matches = re.finditer(r'## 🎬 \[Event Scene (\d+):\s*([^\]]*)\]\n([\s\S]*?)(?=\n##|\n---|$)', content)
    for m in ev_matches:
        evnum = int(m.group(1))
        body = m.group(3).strip()
        events_stories[evnum] = body

    return intro_story, outro_story, qs_stories, events_stories

def get_unit_from_builder(filename):
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

def main():
    builders_dir = str(paths.ROOT_DIR / "scripts" / "builders")
    generated_dir = paths.ROOT_DIR / "storyboards" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(os.listdir(builders_dir))
    
    for filename in files:
        if not filename.startswith("update_app_") or not filename.endswith(".py"):
            continue
            
        if "update_mobile_css" in filename:
            continue
            
        unit = get_unit_from_builder(filename)
        if not unit:
            continue
            
        grade_str = "grade1" if "m1_" in unit else ("grade2" if "m2_" in unit else "grade3")
        
        yaml_path = Path(game_data_root) / grade_str / f"{unit}.yaml"
        script_path = Path(stories_dir) / grade_str / f"{unit}_script.md"
        
        target_sb_dir = generated_dir / grade_str
        target_sb_dir.mkdir(parents=True, exist_ok=True)
        target_sb_path = target_sb_dir / f"{unit}_storyboard.md"

        print(f"Processing storyboard for {unit}...")

        # 이미지 에셋 매핑용 폴더명
        assets_folder = None
        for dname in os.listdir(apps_assets_root):
            if dname.startswith(unit) and os.path.isdir(os.path.join(apps_assets_root, dname)):
                assets_folder = dname
                break
        if not assets_folder:
            assets_folder = unit

        if yaml_path.exists() and script_path.exists():
            # ====================================================
            # [신규 아키텍처]: script.md + game_data.yaml 병합 생성
            # ====================================================
            print(f"  -> Using Single Source of Truth [script.md + {unit}.yaml]")
            
            with open(yaml_path, 'r', encoding='utf-8') as y_file:
                gdata = yaml.safe_load(y_file)
                
            # 스키마 필드 체크
            for k in gdata.keys():
                if k not in ALLOWED_YAML_FIELDS:
                    print(f"  [Warning] YAML key '{k}' ignored by schema.")
            
            intro_story, outro_story, qs_stories, events_stories = parse_script_md(script_path)
            
            sb_content = []
            theme_title = assets_folder.replace(f"{unit}_", "").replace("_", " ").title()
            sb_content.append(f"# {grade_str} {int(unit[3:5])}단원 대본집: {theme_title}")
            sb_content.append("\n이 파일은 수학 방탈출 게임의 스토리 대사, 퀴즈 문항, 이벤트 씬 정보를 관리하는 원천 데이터 파일입니다.\n")
            sb_content.append("---")
            
            # 이미지 매핑
            sb_content.append("\n# [이미지 매핑]")
            img_map = gdata.get("image_mapping", {})
            sb_content.append(f"- intro: {img_map.get('intro', 'intro.png')}")
            for i in range(1, 21):
                sb_content.append(f"- {i}: {img_map.get(f'q{i}', f'q{i}.png')}")
            for i in range(1, 5):
                sb_content.append(f"- event{i}: {img_map.get(f'event{i}', f'event{i}.png')}")
            sb_content.append(f"- outro: {img_map.get('outro', 'outro.png')}")
            sb_content.append("\n---")
            
            # 문항 정의
            sb_content.append("\n# [문항 정의]")
            q_meta = gdata.get("questions", {})
            for i in range(1, 21):
                qkey = f"q{i}"
                meta = q_meta.get(qkey, {})
                title = meta.get("title", f"수수께끼 {i}")
                qtext = meta.get("qtext", "")
                hint = meta.get("hint", "")
                ans_check = meta.get("ans_check", "")
                placeholder = meta.get("placeholder", "숫자 입력")
                error = meta.get("error", "틀렸습니다.")
                options = meta.get("options", [])
                extra_class = meta.get("extra_class", "")
                
                story_body = qs_stories.get(i, f"[{unit.upper()}]: 지문 로드 실패")
                
                sb_content.append(f"\n## Q{i}")
                sb_content.append(f"- 제목: {title}")
                sb_content.append(f"- 이미지: ![{title}](../../apps/assets/{assets_folder}/{img_map.get(qkey, f'q{i}.png')})")
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
                sb_content.append(story_body)
                
            # 이벤트 정의
            sb_content.append("\n---")
            sb_content.append("\n# [이벤트 정의]")
            ev_meta = gdata.get("events", {})
            for i in range(1, 5):
                evkey = f"event{i}"
                meta = ev_meta.get(evkey, {})
                title = meta.get("title", "돌발 이벤트")
                btn = meta.get("btn_text", "계속하기")
                nxt = meta.get("next_stage", "outro")
                prog = meta.get("progress", 25)
                
                story_body = events_stories.get(i, f"[조력자]: 이벤트 지문 로드 실패")
                
                sb_content.append(f"\n## EVENT{i}")
                sb_content.append(f"- 제목: {title}")
                sb_content.append(f"- 이미지: ![이벤트{i}](../../apps/assets/{assets_folder}/{img_map.get(evkey, f'event{i}.png')})")
                sb_content.append(f"- 버튼 텍스트: {btn}")
                sb_content.append(f"- 다음 스테이지: {nxt}")
                sb_content.append(f"- 달성도: {prog}")
                sb_content.append("- 지문:")
                sb_content.append(story_body)
                
            with open(target_sb_path, 'w', encoding='utf-8') as sf:
                sf.write('\n'.join(sb_content))
                
        else:
            # ====================================================
            # [레거시 호환성 fallback]: 기존 storyboards/ 에서 복사 이송
            # ====================================================
            legacy_src_path = paths.ROOT_DIR / "storyboards" / grade_str / f"{unit}_storyboard.md"
            if legacy_src_path.exists():
                print(f"  -> [Legacy Fallback] Copying existing storyboard from {legacy_src_path.name}")
                shutil.copy2(str(legacy_src_path), str(target_sb_path))
            else:
                print(f"  [Warning] Legacy storyboard source not found: {legacy_src_path}")

    print("[+] Storyboard generation process completed successfully.")

if __name__ == "__main__":
    main()
