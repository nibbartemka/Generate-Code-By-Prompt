from abc import ABC, abstractmethod
from typing import List

from lexer import LexemInfo


class Prompt(ABC):
    lexem_info: List[LexemInfo] = []

    @classmethod
    @abstractmethod
    def get_lexem_info(cls) -> List[LexemInfo]:
        pass

    @abstractmethod
    def to_python(self) -> str:
        pass

    @abstractmethod
    def to_java(self) -> str:
        pass
