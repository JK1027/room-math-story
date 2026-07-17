import os
import re
from pathlib import Path

def load_storyboard_qs(unit):
    # --- Central Configs Loading ---
    import sys
    _cur = os.path.dirname(os.path.abspath(__file__))
    _root = os.path.dirname(os.path.dirname(os.path.dirname(_cur)))
    if _root not in sys.path:
        sys.path.append(_root)
    from scripts.config import paths
    
    grade_dir = "grade1" if "m1_" in unit else ("grade2" if "m2_" in unit else "grade3")
    storyboard_path = str(paths.ROOT_DIR / "storyboards" / "generated" / grade_dir / f"{unit}_storyboard.md")
    if not os.path.exists(storyboard_path):
        storyboard_path = str(paths.storyboard_path(grade_dir, unit))
        
    if not os.path.exists(storyboard_path):
        raise FileNotFoundError(f"Storyboard file not found for unit '{unit}' at {storyboard_path}")
        
    with open(storyboard_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    qs = []
    
    # Q 단위 파싱
    q_parts = content.split('## Q')
    for part in q_parts[1:]:
        part_lines = part.strip().split('\n')
        qnum_str = part_lines[0].strip()
        if not qnum_str.isdigit():
            continue
        qnum = int(qnum_str)
        
        q_data = {"qnum": qnum}
        story_started = False
        story_lines = []
        
        for line in part_lines[1:]:
            if story_started:
                # 다음 문항이나 이벤트, 구분선이 나오면 종료
                if line.strip().startswith('---') or line.strip().startswith('# ['):
                    break
                story_lines.append(line)
                continue
                
            line_str = line.strip()
            if line_str.startswith('- 제목:'):
                q_data["title"] = line_str.replace('- 제목:', '').strip()
            elif line_str.startswith('- 질문:'):
                q_data["qtext"] = line_str.replace('- 질문:', '').strip()
            elif line_str.startswith('- 힌트:'):
                q_data["hint"] = line_str.replace('- 힌트:', '').strip()
            elif line_str.startswith('- 정답 체크:'):
                q_data["ans_check"] = line_str.replace('- 정답 체크:', '').strip()
            elif line_str.startswith('- 플레이스홀더:'):
                q_data["placeholder"] = line_str.replace('- 플레이스홀더:', '').strip()
            elif line_str.startswith('- 에러 메시지:'):
                q_data["error"] = line_str.replace('- 에러 메시지:', '').strip()
            elif line_str.startswith('- extra_class:'):
                q_data["extra_class"] = line_str.replace('- extra_class:', '').strip()
            elif line_str.startswith('- 선택지:'):
                opts_str = line_str.replace('- 선택지:', '').strip()
                q_data["options"] = [opt.strip() for opt in opts_str.split(',') if opt.strip()]
            elif line_str.startswith('- 지문:'):
                story_started = True
                
        # 대화 지문 결합 및 정리
        q_data["story"] = '\n'.join(story_lines).strip()
        qs.append(q_data)
        
    # qnum 오름차순 정렬 보장
    qs.sort(key=lambda x: x["qnum"])
    return qs
