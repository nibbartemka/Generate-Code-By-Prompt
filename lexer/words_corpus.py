from typing import Dict

from .lexem import LexemInfo


CORPUS: Dict[str, LexemInfo] = {
    'оставить': LexemInfo.FILTER_STAY,
    'сохранить': LexemInfo.FILTER_STAY,
    'убрать': LexemInfo.FILTER_REMOVE,
    'исключить': LexemInfo.FILTER_REMOVE,
    'удалить': LexemInfo.FILTER_REMOVE,
    'найти': LexemInfo.SEARCH,
    'определить': LexemInfo.SEARCH,
    'выписать': LexemInfo.SEARCH,
    'прочитать': LexemInfo.READ,
    'просмотреть': LexemInfo.READ,
    'многопоток': LexemInfo.MULTITHREADING,
    'от': LexemInfo.FROM,
    'до': LexemInfo.TO,
    'div': LexemInfo.HTML_TAG,
    'a': LexemInfo.HTML_TAG,
    'p': LexemInfo.HTML_TAG
}
