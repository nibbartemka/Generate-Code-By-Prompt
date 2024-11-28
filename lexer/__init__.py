""" Lexer

Данный пакет представляет релализацию лексера, позволяющего выделить
из текста ключевые слова

Modules:
- lexem: модуль, в котором объявляется класс лексемы и определяются их типы.
- lexer: модуль, в котором представлена реализация лексера.
- similarity_estimator: модуль, в котором описывается класс, 
позволяющий оценить "близость" слов.
- words_corpus: модуль, в котором представлен перечень словарь, 
используемый в рамках поиска ключевых слов.
"""


from .lexer import Lexer, Lexem, LexemInfo
from .similarity_estimator import (LevensteinSimilarityEstimator,
                                   LinesSimilarityEstimator)
