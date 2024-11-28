from enum import Enum
from dataclasses import dataclass


class LexemInfo(Enum):
    FILTER_STAY = "FILTER_STAY"
    FILTER_REMOVE = "FILTER_REMOVE"
    SEARCH = "SEARCH"
    READ = "READ"
    LIST = "LIST"
    FROM = "FROM"
    TO = "TO"
    HTML_TAG = "HTML_TAG"
    INTEGER = "INTEGER"
    URL = "URL"
    FILE = "FILE"
    MULTITHREADING = "MULTITHREADING"


@dataclass(slots=True, frozen=True)
class Lexem:
    lexem_info: LexemInfo
    value: str
