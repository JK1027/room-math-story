"""
migrate_to_chapter.py - 기존 23개 단원의 script.md와 quiz_data.yaml을 단일 chapterXX.md로 일괄 자동 통합
"""
import os
import sys
import re
import yaml
from pathlib import Path

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(_cur))
if _root not in sys.path:
    sys.path.append(_root)
from scripts.config import paths
from scripts.config.constants import SUPPORTED_GRADES

def read_file_safe(filepath):
    """인코딩을 판별하여 파일을 안전하게 로드합니다."""
    for enc in ['utf-8-sig', 'utf-8', 'cp949']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read().replace('\r\n', '\n')
        except UnicodeDecodeError:
            continue
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read().replace('\r\n', '\n')

def parse_script_md(content):
    """기존 대본집 마크다운에서 인트로, 아웃트로, Q1~Q20의 스토리 지문, Event 1~4 지문을 추출합니다."""
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
        story_match = re.search(r'-\s*(?:\*\*스토리\*\*:\s*|\*\*스토리:\*\*\s*|스토리\s*:\s*)([\s\S]*)', body)
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

def main():
    print("====================================================")
    print("  수학 방탈출 단일 원본(chapterXX.md) 통합 마이그레이션")
    print("====================================================")
    
    quiz_data_root = paths.ROOT_DIR / "quiz_data"
    stories_root = paths.STORIES_DIR
    
    migrated_count = 0
    
    for g in SUPPORTED_GRADES:
        meta_file = stories_root / g / "metadata.yaml"
        if not meta_file.exists():
            print(f"[-] Warning: metadata.yaml not found for {g}")
            continue
            
        with open(meta_file, 'r', encoding='utf-8') as mf:
            meta_data = yaml.safe_load(mf)
            
        units_meta = meta_data.get("units", {})
        
        for unit_id, u_meta in units_meta.items():
            print(f"Migrating {unit_id}...")
            
            # 1. 원본 파일 로드
            yaml_path = quiz_data_root / g / f"{unit_id}.yaml"
            script_path = stories_root / g / f"{unit_id}_script.md"
            
            if not yaml_path.exists() or not script_path.exists():
                print(f"  [Skip] YAML or Script missing for {unit_id}")
                continue
                
            yaml_raw = yaml.safe_load(read_file_safe(yaml_path))
            script_raw = read_file_safe(script_path)
            
            # 2. 내용 파싱
            intro_story, outro_story, qs_stories, events_stories = parse_script_md(script_raw)
            
            # 3. 새로운 chapterXX.md 포맷 구성
            chapter_num = unit_id[3:5] # m1_02 -> 02
            target_file_path = stories_root / g / f"chapter{chapter_num}.md"
            
            image_mapping = yaml_raw.get("image_mapping", {})
            questions_meta = yaml_raw.get("questions", {})
            events_meta = yaml_raw.get("events", {})
            
            # --- Frontmatter ---
            char_meta = u_meta.get("characters", {})
            frontmatter = f"""---
title: "{u_meta.get('title', '')}"
template: "{yaml_raw.get('template', 'escape_room')}"
hero: "{char_meta.get('hero', '')}"
helper: "{char_meta.get('helper', '')}"
villain: "{char_meta.get('villain', '')}"
intro_image: "{image_mapping.get('intro', 'intro.png')}"
outro_image: "{image_mapping.get('outro', 'outro.png')}"
---
"""
            
            chapter_body = []
            chapter_body.append(frontmatter)
            
            # --- Intro ---
            chapter_body.append("## 🎬 [오프닝 & 인트로]\n")
            chapter_body.append(intro_story + "\n")
            
            # --- Questions 1 ~ 20 ---
            for i in range(1, 21):
                qkey = f"q{i}"
                q_meta = questions_meta.get(qkey, {})
                
                title = q_meta.get("title", f"수수께끼 {i}")
                qtext = q_meta.get("qtext", "")
                hint = q_meta.get("hint", "")
                ans_check = q_meta.get("ans_check", "")
                placeholder = q_meta.get("placeholder", "숫자 입력")
                error_msg = q_meta.get("error", "틀렸습니다.")
                options = q_meta.get("options", [])
                extra_class = q_meta.get("extra_class", "")
                
                story_body = qs_stories.get(i, "")
                
                q_block = f"""## Q{i}

### Title
{title}

### Image
{image_mapping.get(qkey, f'q{i}.png')}

### Question
{qtext}
"""
                if options:
                    choices_block = "\n".join([f"- {opt}" for opt in options])
                    q_block += f"\n### Choices\n{choices_block}\n"
                    
                q_block += f"""
### Answer
{ans_check}

### Placeholder
{placeholder}

### Error Message
{error_msg}

### Hint
{hint}
"""
                if extra_class:
                    q_block += f"\n### Extra Class\n{extra_class}\n"
                    
                q_block += f"""
### Story
{story_body}
"""
                chapter_body.append(q_block)
                
            # --- Events 1 ~ 4 ---
            for i in range(1, 5):
                evkey = f"event{i}"
                ev_meta = events_meta.get(evkey, {})
                
                title = ev_meta.get("title", "돌발 이벤트")
                btn_text = ev_meta.get("btn_text", "계속하기")
                next_stage = ev_meta.get("next_stage", "outro")
                progress = ev_meta.get("progress", 25)
                story_body = events_stories.get(i, "")
                
                ev_block = f"""## EVENT{i}

### Title
{title}

### Image
{image_mapping.get(evkey, f'event{i}.png')}

### Button Text
{btn_text}

### Next Stage
{next_stage}

### Progress
{progress}

### Story
{story_body}
"""
                chapter_body.append(ev_block)
                
            # --- Outro ---
            chapter_body.append("## 🎬 [엔딩 & 아웃트로]\n")
            chapter_body.append(outro_story + "\n")
            
            # 4. 파일 쓰기
            with open(target_file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(chapter_body))
                
            print(f"  [OK] Saved to: {target_file_path.name}")
            migrated_count += 1
            
    print(f"\n====================================================")
    print(f"  마이그레이션이 완료되었습니다! (총 {migrated_count}개 장 이주 완료)")
    print("====================================================")

if __name__ == "__main__":
    main()
