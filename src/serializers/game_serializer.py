from typing import Dict, Any, List
from src.domain.models import Chapter

class GameSerializer:
    """
    [Game Serializer] Chapter 도메인 객체를 웹게임 런타임에 주입할 
    GAME_DATA JSON 딕셔너리 구조로 안전하게 직렬화합니다.
    """
    
    @staticmethod
    def serialize(chapter: Chapter, grade_str: str, unit_code: str) -> Dict[str, Any]:
        
        # 1. 문항 리스트 직렬화
        serialized_questions: List[Dict[str, Any]] = []
        for q in chapter.questions:
            serialized_questions.append({
                "qnum": q.qnum,
                "title": q.title,
                "image": q.image,
                "qtext": q.qtext,
                "choices": list(q.choices),
                "answer": q.answer, # 구조화된 dict {"type": "...", "values": [...]}
                "placeholder": q.placeholder,
                "error_message": q.error_message,
                "hint": q.hint,
                "story": q.story,
                "extra_class": q.extra_class
            })
            
        # 2. 이벤트 리스트 직렬화
        serialized_events: List[Dict[str, Any]] = []
        for ev in chapter.events:
            serialized_events.append({
                "evnum": ev.evnum,
                "title": ev.title,
                "image": ev.image,
                "btn_text": ev.btn_text,
                "next_stage": ev.next_stage,
                "progress": ev.progress,
                "story": ev.story
            })
            
        # 3. 전역 JSON 데이터 조립
        game_data = {
            "unit_code": unit_code,
            "grade": grade_str,
            "title": chapter.title,
            "template": chapter.template,
            "hero": chapter.hero,
            "helper": chapter.helper,
            "villain": chapter.villain,
            "timer_limit_sec": 2400, # 기본값 40분
            "intro": {
                "image": chapter.intro_image,
                "story": chapter.intro_story
            },
            "outro": {
                "image": chapter.outro_image,
                "story_success": f"축하합니다! 모든 {chapter.helper} 봉인을 해제하고 수학 탈출 좌표를 복원했습니다.",
                "story_failure": "시간이 모두 고갈되었습니다! 탈출에 실패했습니다."
            },
            "questions": serialized_questions,
            "events": serialized_events
        }
        
        return game_data
