import os
import re
import yaml
from typing import List, Tuple, Dict, Any, Optional
from src.domain.models import Chapter, Question, Event
from src.parser.result import ParseResult

def read_file_safe(filepath: str) -> str:
    """안전하게 파일을 디코딩하여 텍스트로 로드합니다."""
    for enc in ['utf-8-sig', 'utf-8', 'cp949']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read().replace('\r\n', '\n')
        except UnicodeDecodeError:
            continue
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read().replace('\r\n', '\n')

def extract_section_text(content: str, header: str, next_headers: List[str]) -> str:
    """특정 3단계 헤더(### Header) 아래부터 다음 헤더(### or ##) 전까지의 텍스트를 추출합니다."""
    escaped_header = re.escape(header)
    pattern = rf"{escaped_header}\n([\s\S]*?)(?=(?:\n### |\n## |\n---|$))"
    match = re.search(pattern, content)
    return match.group(1).strip() if match else ""

def parse_choices(choices_text: str) -> Tuple[str, ...]:
    """Choices 아래의 마크다운 리스트(- 선택지)를 파싱하여 튜플로 반환합니다."""
    choices = []
    for line in choices_text.split('\n'):
        line_clean = line.strip()
        if not line_clean:
            continue
        # - 나 * 로 시작하는 아이템 탐색
        match = re.match(r'^[-*+]\s+(.*)$', line_clean)
        if match:
            choices.append(match.group(1).strip().strip('"\''))
        else:
            choices.append(line_clean.strip().strip('"\''))
    return tuple(choices)

def parse_chapter(filepath: str) -> ParseResult:
    """
    [SSoT 파서 코어] chapterXX.md 파일을 읽어 Heading 기반 DSL 명세에 맞춰
    Chapter 도메인 객체를 합성합니다.
    """
    errors: List[str] = []
    warnings: List[str] = []
    
    if not os.path.exists(filepath):
        errors.append(f"Source file not found: {filepath}")
        return ParseResult(chapter=None, errors=errors, warnings=warnings)
        
    content = read_file_safe(filepath)
    
    # 1. Frontmatter 파싱
    frontmatter_match = re.match(r'^---\n([\s\S]*?)\n---\n', content)
    if not frontmatter_match:
        errors.append("Missing Frontmatter configuration in chapter source.")
        return ParseResult(chapter=None, errors=errors, warnings=warnings)
        
    frontmatter_raw = frontmatter_match.group(1)
    body_content = content[frontmatter_match.end():].strip()
    
    try:
        meta = yaml.safe_load(frontmatter_raw) or {}
    except Exception as e:
        errors.append(f"Failed to parse YAML frontmatter: {e}")
        return ParseResult(chapter=None, errors=errors, warnings=warnings)
        
    # 필수 메타데이터 체크
    required_meta = ["title", "template", "hero", "helper", "villain", "intro_image", "outro_image"]
    for field in required_meta:
        if field not in meta or not meta[field]:
            errors.append(f"Missing required metadata field: '{field}'")
            
    # 2. 오프닝 및 인트로 대본 파싱
    intro_match = re.search(r'## 🎬 \[오프닝 & 인트로\]\n([\s\S]*?)(?=(?:\n## |$))', body_content)
    intro_story = intro_match.group(1).strip() if intro_match else ""
    if not intro_story:
        warnings.append("Opening & Intro story section is empty.")
        
    # 3. 엔딩 및 아웃트로 대본 파싱
    outro_match = re.search(r'## 🎬 \[엔딩 & 아웃트로\]\n([\s\S]*?)(?=(?:\n## |$))', body_content)
    outro_story = outro_match.group(1).strip() if outro_match else ""
    if not outro_story:
        warnings.append("Ending & Outro story section is empty.")

    # 4. Q1 ~ Q20 퀴즈 데이터 추출
    questions: List[Question] = []
    for qnum in range(1, 21):
        # Q[번호] 헤더와 다음 Q[번호] 헤더 또는 EVENT1 헤더 전까지 획득
        q_pattern = rf"## Q{qnum}\n([\s\S]*?)(?=(?:\n## Q{qnum+1}\n|\n## EVENT1\n|\n## 🎬 \[엔딩 & 아웃트로\]|$))"
        q_match = re.search(q_pattern, body_content)
        
        if not q_match:
            errors.append(f"Section ## Q{qnum} is missing or improperly placed.")
            continue
            
        q_block = q_match.group(1)
        
        title = extract_section_text(q_block, "### Title", ["### Image", "### Question"])
        image = extract_section_text(q_block, "### Image", ["### Question"])
        qtext = extract_section_text(q_block, "### Question", ["### Choices", "### Answer"])
        choices_raw = extract_section_text(q_block, "### Choices", ["### Answer"])
        answer = extract_section_text(q_block, "### Answer", ["### Placeholder"])
        placeholder = extract_section_text(q_block, "### Placeholder", ["### Error Message"])
        error_msg = extract_section_text(q_block, "### Error Message", ["### Hint"])
        hint = extract_section_text(q_block, "### Hint", ["### Story", "### Extra Class"])
        extra_class = extract_section_text(q_block, "### Extra Class", ["### Story"])
        story = extract_section_text(q_block, "### Story", [])
        
        choices = parse_choices(choices_raw)
        
        # 퀴즈 내부 필수 필드 검증 (구조 파싱 확인 차원)
        if not title:
            errors.append(f"Q{qnum}: '### Title' is missing.")
        if not qtext:
            errors.append(f"Q{qnum}: '### Question' text is missing.")
        if not answer:
            errors.append(f"Q{qnum}: '### Answer' validation formula is missing.")
            
        questions.append(Question(
            qnum=qnum,
            title=title,
            image=image,
            qtext=qtext,
            choices=choices,
            answer=answer,
            placeholder=placeholder,
            error_message=error_msg,
            hint=hint,
            story=story,
            extra_class=extra_class
        ))
        
    # 5. EVENT1 ~ EVENT4 이벤트 데이터 추출
    events: List[Event] = []
    for evnum in range(1, 5):
        next_ev_header = f"## EVENT{evnum+1}" if evnum < 4 else "## 🎬 \\[엔딩 & 아웃트로\\]"
        ev_pattern = rf"## EVENT{evnum}\n([\s\S]*?)(?=(?:\n{next_ev_header}\n|\n## 🎬 \[엔딩 & 아웃트로\]|$))"
        ev_match = re.search(ev_pattern, body_content)
        
        if not ev_match:
            errors.append(f"Section ## EVENT{evnum} is missing or improperly placed.")
            continue
            
        ev_block = ev_match.group(1)
        
        title = extract_section_text(ev_block, "### Title", ["### Image"])
        image = extract_section_text(ev_block, "### Image", ["### Button Text"])
        btn_text = extract_section_text(ev_block, "### Button Text", ["### Next Stage"])
        next_stage = extract_section_text(ev_block, "### Next Stage", ["### Progress"])
        progress_raw = extract_section_text(ev_block, "### Progress", ["### Story"])
        story = extract_section_text(ev_block, "### Story", [])
        
        progress = 25
        if progress_raw:
            try:
                progress = int(progress_raw)
            except ValueError:
                errors.append(f"EVENT{evnum}: Progress value '{progress_raw}' must be an integer.")
                
        if not title:
            errors.append(f"EVENT{evnum}: '### Title' is missing.")
        if not btn_text:
            errors.append(f"EVENT{evnum}: '### Button Text' is missing.")
            
        events.append(Event(
            evnum=evnum,
            title=title,
            image=image,
            btn_text=btn_text,
            next_stage=next_stage,
            progress=progress,
            story=story
        ))
        
    if errors:
        return ParseResult(chapter=None, errors=errors, warnings=warnings)
        
    # Chapter 도메인 합성
    chapter = Chapter(
        title=meta.get("title", ""),
        template=meta.get("template", "escape_room"),
        hero=meta.get("hero", ""),
        helper=meta.get("helper", ""),
        villain=meta.get("villain", ""),
        intro_image=meta.get("intro_image", "intro.png"),
        outro_image=meta.get("outro_image", "outro.png"),
        intro_story=intro_story,
        outro_story=outro_story,
        questions=tuple(questions),
        events=tuple(events)
    )
    
    return ParseResult(chapter=chapter, errors=errors, warnings=warnings)
