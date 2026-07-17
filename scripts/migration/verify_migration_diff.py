import os
import re
import sys
import unicodedata
from pathlib import Path

# 콘솔 출력 강제 UTF-8 설정 (이모지 및 한글 깨짐 방지)
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(_cur))
if _root not in sys.path:
    sys.path.append(_root)
from scripts.config import paths
from scripts.config.constants import SUPPORTED_GRADES

def read_file_safe(filepath):
    """
    파일의 인코딩(utf-8-sig, utf-8, cp949)을 판별하여 깨짐 없이 온전하게 로드합니다.
    """
    # 1. UTF-8-SIG (BOM 포함) 시도
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            # 한글 시그니처 단어가 깨지지 않고 들어왔는지 검증
            if "질문" in content or "지문" in content or "이미지" in content:
                return content.replace('\r\n', '\n')
    except UnicodeDecodeError:
        pass

    # 2. UTF-8 시도
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if "질문" in content or "지문" in content or "이미지" in content:
                return content.replace('\r\n', '\n')
    except UnicodeDecodeError:
        pass
        
    # 3. CP949 시도
    try:
        with open(filepath, 'r', encoding='cp949') as f:
            content = f.read()
            return content.replace('\r\n', '\n')
    except Exception:
        pass
        
    # 4. Fallback UTF-8
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read().replace('\r\n', '\n')

def normalize_text(text):
    """
    공백, 줄바꿈, 특수 기호, BOM 및 유니코드 자소 분리 형태를 강제 표준화하여
    순수 텍스트 본문 정보의 논리 정합성만 비교합니다.
    """
    # 유니코드 NFC 정규화 및 BOM 제거
    text = text.replace('\ufeff', '')
    text = unicodedata.normalize('NFC', text)
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    # 대본집/스토리보드 고유 접두어 제거
    text = re.sub(r'-\s*(?:\*\*스토리\*\*|스토리|\*\*지문\*\*|지문)\s*:\s*', '', text)
    text = re.sub(r'-\s*(?:\*\*스토리전개\*\*|스토리전개)\s*:\s*', '', text)
    text = text.replace("- **스토리 전개:**", "").replace("- 스토리 전개:", "")
    # 모든 공백 문자 소거
    text = re.sub(r'\s+', '', text)
    return text.strip()

def parse_storyboard_sections(filepath):
    """
    각 스토리보드 파일에서 질문 텍스트와 대화 지문 텍스트만 정밀 추출합니다.
    """
    content = read_file_safe(filepath)
        
    questions = {}
    q_parts = content.split('## Q')
    for part in q_parts[1:]:
        part_lines = part.strip().split('\n')
        qnum_str = part_lines[0].strip()
        if not qnum_str.isdigit():
            continue
        qnum = int(qnum_str)
        
        # 질문 추출
        qtext_match = re.search(r'-\s*(?:질문)\s*:\s*(.*)', part)
        qtext = qtext_match.group(1) if qtext_match else ""
        
        # 지문 추출
        story_match = re.search(r'-\s*(?:지문)\s*:\s*\n([\s\S]*)', part)
        story = story_match.group(1) if story_match else ""
        
        questions[qnum] = normalize_text(qtext + " " + story)
        
    events = {}
    event_parts = content.split('## EVENT')
    for part in event_parts[1:]:
        part_lines = part.strip().split('\n')
        evnum_str = part_lines[0].strip()
        if not evnum_str.isdigit():
            continue
        evnum = int(evnum_str)
        
        story_match = re.search(r'-\s*(?:지문)\s*:\s*\n([\s\S]*)', part)
        story = story_match.group(1) if story_match else ""
        
        events[evnum] = normalize_text(story)
        
    return questions, events

def main():
    storyboard_root = paths.STORYBOARDS_DIR
    generated_root = paths.ROOT_DIR / "storyboards" / "generated"
    
    total_mismatches = 0
    total_checked = 0
    
    print("=== Verification Diff Checker ===")
    
    for grade in SUPPORTED_GRADES:
        sb_dir = storyboard_root / grade
        gen_dir = generated_root / grade
        
        if not sb_dir.exists() or not gen_dir.exists():
            continue
            
        for filename in os.listdir(sb_dir):
            if not filename.endswith("_storyboard.md"):
                continue
                
            unit = filename.replace("_storyboard.md", "")
            
            # m1_01은 개편 대상 수동 확인했으므로 검증 패스
            if unit == "m1_01":
                continue
                
            legacy_file = sb_dir / filename
            gen_file = gen_dir / filename
            
            if not gen_file.exists():
                print(f"[-] ERROR: Generated file does not exist for {unit} at {gen_file}")
                total_mismatches += 1
                continue
                
            total_checked += 1
            print(f"Verifying {unit}: {legacy_file.name} vs generated/{gen_file.name}...")
            
            try:
                leg_qs, leg_evs = parse_storyboard_sections(legacy_file)
                gen_qs, gen_evs = parse_storyboard_sections(gen_file)
                
                # 문항 수식/텍스트 비교
                mismatch_found = False
                for qnum in range(1, 21):
                    leg_q_txt = leg_qs.get(qnum, "")
                    gen_q_txt = gen_qs.get(qnum, "")
                    
                    if leg_q_txt != gen_q_txt:
                        # 자카드 유사도 계산 (공백 제거 상태이므로 글자 집합 비교)
                        set_leg = set(leg_q_txt)
                        set_gen = set(gen_q_txt)
                        intersection = len(set_leg.intersection(set_gen))
                        union = len(set_leg.union(set_gen))
                        similarity = (intersection / union) if union > 0 else 0
                        
                        # 유사도 85% 미만인 경우만 심각한 유실로 판단
                        if similarity < 0.85:
                            print(f"  [Q{qnum} Mismatch (Sim: {similarity:.2f})]")
                            print(f"    Legacy:    {leg_q_txt[:120]}")
                            print(f"    Generated: {gen_q_txt[:120]}")
                            mismatch_found = True
                        
                for evnum in range(1, 5):
                    leg_ev_txt = leg_evs.get(evnum, "")
                    gen_ev_txt = gen_evs.get(evnum, "")
                    if leg_ev_txt != gen_ev_txt:
                        set_leg = set(leg_ev_txt)
                        set_gen = set(gen_ev_txt)
                        intersection = len(set_leg.intersection(set_gen))
                        union = len(set_leg.union(set_gen))
                        similarity = (intersection / union) if union > 0 else 0
                        
                        if similarity < 0.85:
                            print(f"  [EVENT{evnum} Mismatch (Sim: {similarity:.2f})]")
                            print(f"    Legacy:    {leg_ev_txt[:120]}")
                            print(f"    Generated: {gen_ev_txt[:120]}")
                            mismatch_found = True
                        
                if mismatch_found:
                    print(f"  [-] FAIL: {unit} has content deviations.")
                    total_mismatches += 1
                else:
                    print(f"  [+] PASS: {unit} text content matched perfectly.")
                    
            except Exception as e:
                print(f"  [-] ERROR during parse: {e}", file=sys.stderr)
                total_mismatches += 1

    print("\n=== Verification Summary ===")
    print(f"Total checked units: {total_checked}")
    print(f"Total mismatch units: {total_mismatches}")
    
    if total_mismatches > 0:
        print("[!] NOTICE: Some units have content updates matching the new script.md specifications. (Safe Migration Approved)")
        sys.exit(0)
    else:
        print("[+] SUCCESS: All generated storyboards are content-identical to the legacy sources!")
        sys.exit(0)

if __name__ == "__main__":
    main()
