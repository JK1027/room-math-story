from abc import ABC, abstractmethod
from src.models import Chapter

class Builder(ABC):
    """
    [Builder Interface] 모든 스토리 빌더(Storybook, Game)가 구현해야 하는 
    공통 추상 베이스 클래스입니다.
    """
    
    @abstractmethod
    def build(self, chapter: Chapter, grade_str: str, unit_code: str) -> bool:
        """
        주어진 도메인 객체(Chapter) 정보를 읽어 전용 산출물(HTML 뷰어 또는 게임 앱)을 생성합니다.
        
        Args:
            chapter: 읽기 전용으로 가용할 불변 Chapter 도메인 객체
            grade_str: 학년 코드 (예: "grade1")
            unit_code: 단원 코드 (예: "m1_02")
        Returns:
            True 빌드 성공, False 빌드 실패
        """
        pass
