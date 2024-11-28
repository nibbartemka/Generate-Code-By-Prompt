from typing import Optional, List
import re

from .lexem import Lexem, LexemInfo
from .words_corpus import CORPUS
from .similarity_estimator import LinesSimilarityEstimator


class Lexer(object):
    MIN_SIMILARITY_COEFFICIENT: float = 0.5

    def __init__(self, text: str,
                 similarity_estimator: LinesSimilarityEstimator) -> None:
        self.text: str = text
        self.similarity_estimator: LinesSimilarityEstimator = similarity_estimator

    def get_all_lexem(self) -> List[Lexem]:
        """ Метод для получения всех лексем из текста

        Note:
            Аргумент `self` не входит в секцию `Args`

        Args:

        Returns:
            List[Lexem]: Пустой или непустой список лексем
        """

        all_lexem: List[Lexem] = []
        words: List[str] = self.__extract_words(self.text)
        for word in words:
            word = word.strip(',. !?')
            lexem: Optional[Lexem] = self.__get_lexem(word)
            if lexem:
                all_lexem.extend([lexem])

        return all_lexem

    def __extract_words(self, line: str) -> List[str]:
        """ Метод для получения списка слов из строки

        Note:
            Аргумент `self` не входит в секцию `Args`

        Args:
            line (str): строка, из которой нужно извлечь слова

        Returns:
            List[str]: Список строк. Список может оказаться пустым, 
            если строка пуста
        """

        words: List[str] = re.findall(r'\[.*?\]|\S+', line)
        return words

    def __get_lexem(self, word: str) -> Optional[Lexem]:
        """ Метод для получения лексемы из слова

        Note:
            Аргумент `self` не входит в секцию `Args`

        Args:
            word (str): слово, из которого нужно извлечь лексему

        Returns:
            Optional[Lexem]: None, если из слова невозможно извлечь лексему,
            иначе объект класса Lexem
        """

        if word.isnumeric():
            return Lexem(LexemInfo.INTEGER, word)

        if self.__is_valid_file(word):
            return Lexem(LexemInfo.FILE, word)

        if self.__is_valid_url(word):
            url: str = word
            if not url.startswith('https://'):
                url = 'https://' + url
            return Lexem(LexemInfo.URL, url)

        if self.__is_valid_list(word):
            return Lexem(LexemInfo.LIST, word)

        similar_word: Optional[str] = None
        max_similarity_score: float = 0.0

        for corpus_word in CORPUS:
            similarity_score: float = (self.similarity_estimator
                                           .get_similarity_score(word, corpus_word))

            if similarity_score > max_similarity_score:
                max_similarity_score = similarity_score
                similar_word = corpus_word

        if (similar_word is not None
           and max_similarity_score > self.MIN_SIMILARITY_COEFFICIENT):
            return Lexem(CORPUS[similar_word], similar_word)

    def __is_valid_file(self, line: str) -> bool:
        """ Метод проверки соответствия строки шаблону наименования файла

        Note:
            Аргумент `self` не входит в секцию `Args`

        Args:
            line (str): строка, которую нужно проверить

        Returns:
             bool: True, если строка совпадает с шаблоном наименования файла,
             иначе False
        """

        pattern: str = r'^[a-zA-Z0-9_а-яА-Я\- ]+\.(pdf|txt|json|xlsx)$'
        return bool(re.match(pattern, line))

    def __is_valid_url(self, line: str) -> bool:
        """ Метод проверки соответствия строки шаблону url-адреса

        Note:
            Аргумент `self` не входит в секцию `Args`

        Args:
            line (str): строка, которую нужно проверить

        Returns:
             bool: True, если строка совпадает с шаблоном url-адреса,
             иначе False
        """

        pattern: str = r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.(ru|com|su))(/[^\s]*)?$'
        return bool(re.match(pattern, line))

    def __is_valid_list(self, line: str) -> bool:
        """ Метод проверки соответствия строки шаблону списка

        Note:
            Аргумент `self` не входит в секцию `Args`

        Args:
            line (str): строка, которую нужно проверить

        Returns:
             bool: True, если строка совпадает с шаблоном списка,
             иначе False
        """

        pattern: str = r'^\[(\d+(,\s*\d+)*)?\]$'
        return bool(re.match(pattern, line))
