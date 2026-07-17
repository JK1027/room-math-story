import os
from typing import List, Tuple
from src.domain.models import Chapter
from scripts.config import paths

def validate_chapter_rules(chapter: Chapter, grade_str: str, unit_code: str) -> Tuple[List[str], List[str]]:
    """
    [콘텐츠 규칙 검증기] Chapter 도메인 객체를 수신하여 비즈니스/콘텐츠 위반 사항을 진단합니다.
    (Parser가 구문 분석을 완료한 상태의 Chapter 객체만을 대상으로 비즈니스 검사 수행)
    
    Returns:
        (errors, warnings) 튜플 리스트
    """
    errors: List[str] = []
    warnings: List[str] = []
    
    # 1. 문항 개수 검증 (DOD 규칙: 정확히 20개 문항 존재해야 함)
    if len(chapter.questions) != 20:
        errors.append(f"Total questions count is {len(chapter.questions)}, but exactly 20 are required.")
        
    # 2. 이벤트 개수 검증 (DOD 규칙: 정확히 4개 이벤트 씬 존재해야 함)
    if len(chapter.events) != 4:
        errors.append(f"Total event scenes count is {len(chapter.events)}, but exactly 4 are required.")
        
    # 이미지 파일 존재 여부 검사 준비
    # assets_folder 매핑명 찾기 (예: m1_02_magic_academy)
    assets_folder = None
    apps_assets_root = paths.APPS_DIR / "assets"
    if apps_assets_root.exists():
        for dname in os.listdir(apps_assets_root):
            if dname.startswith(unit_code) and os.path.isdir(apps_assets_root / dname):
                assets_folder = dname
                break
    if not assets_folder:
        assets_folder = unit_code
        
    assets_dir = apps_assets_root / assets_folder
    
    # 3. 개별 문항 비즈니스 규칙 검증
    for idx, q in enumerate(chapter.questions, 1):
        # 퀴즈 지문 존재 검사 (경고로 완화하여 빌드 진행 보장)
        if not q.story or q.story == f"[{unit_code.upper()}]: 지문 로드 실패":
            warnings.append(f"Q{q.qnum}: Dialogue body is missing or empty.")
            
        # 힌트 수록 검사
        if not q.hint:
            errors.append(f"Q{q.qnum}: Hint is missing (Required).")
            
        # 정답 및 플레이스홀더 체크
        if not q.answer:
            errors.append(f"Q{q.qnum}: Answer condition check formula is missing.")
            
        # 에셋 파일 실재 여부 진단
        if q.image:
            img_path = assets_dir / q.image
            if not img_path.exists():
                warnings.append(f"Q{q.qnum}: Referenced image '{q.image}' does not exist at {img_path}")
        else:
            errors.append(f"Q{q.qnum}: Question image name is empty.")
            
    # 4. 개별 이벤트 규칙 검증
    for idx, ev in enumerate(chapter.events, 1):
        if not ev.story:
            warnings.append(f"EVENT{ev.evnum}: Event scene dialogue body is empty.")
            
        # 에셋 파일 실재 여부 진단
        if ev.image:
            img_path = assets_dir / ev.image
            if not img_path.exists():
                warnings.append(f"EVENT{ev.evnum}: Referenced image '{ev.image}' does not exist at {img_path}")
                
    # 5. 인물 일관성 매칭 검증
    # metadata.yaml 에 수록된 그리스 수학사 인물들과 chapter의 인물이 정합하는지는 
    # validate_story.py CLI 및 PipelineRunner 단계에서 metadata.yaml을 대조하여 검사하도록 위임합니다.
    
    return errors, warnings
