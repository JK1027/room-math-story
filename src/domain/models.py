from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Question:
    qnum: int
    title: str
    image: str
    qtext: str
    choices: Tuple[str, ...]
    answer: str
    placeholder: str
    error_message: str
    hint: str
    story: str
    extra_class: str = ""

@dataclass(frozen=True)
class Event:
    evnum: int
    title: str
    image: str
    btn_text: str
    next_stage: str
    progress: int
    story: str

@dataclass(frozen=True)
class Chapter:
    title: str
    template: str
    hero: str
    helper: str
    villain: str
    intro_image: str
    outro_image: str
    intro_story: str
    outro_story: str
    questions: Tuple[Question, ...]
    events: Tuple[Event, ...]
