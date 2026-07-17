from dataclasses import dataclass
from typing import List, Optional
from src.models import Chapter

@dataclass(frozen=True)
class ParseResult:
    chapter: Optional[Chapter]
    errors: List[str]
    warnings: List[str]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0
