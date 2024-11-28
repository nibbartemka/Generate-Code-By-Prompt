from abc import ABC, abstractmethod


class LinesSimilarityEstimator(ABC):
    @staticmethod
    @abstractmethod
    def estimate(cls, first_line: str, second_line: str) -> int | float:
        pass

    @classmethod
    @abstractmethod
    def get_similarity_score(cls, first_line: str, second_line: str) -> float:
        pass


class LevensteinSimilarityEstimator(LinesSimilarityEstimator):
    MIN_SIMILARITY_COEFFICIENT: float = 0.4

    @staticmethod
    def estimate(first_line: str, second_line: str) -> int:
        """ Метод, позволяющий оценить разницу между строками, 
        выражающуюся в минимальном количестве операций, которые нужно применить, 
        чтобы из первой строки получить вторую

        Args:
            first_line (str): первая строка
            second_line (str): вторая строка

        Returns:
            int: минимальное кол-во операций необходимых
            для преобразования `first_line` в `second_line`
        """

        n, m = len(first_line), len(second_line)

        if n > m:
            first_line, second_line = second_line, first_line
            n, m = m, n

        current_row = range(n + 1)

        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = (previous_row[j] + 1,
                                       current_row[j - 1] + 1,
                                       previous_row[j - 1])

                if first_line[j - 1] != second_line[i - 1]:
                    change += 1

                current_row[j] = min(add, delete, change)

        return current_row[n]

    @classmethod
    def get_similarity_score(cls, first_line: str, second_line: str) -> float:
        """ Метод, позволяющий получить значение
        схожести строк в пределах от 0 до 1

        Args:
            first_line (str): первая строка
            second_line (str): вторая строка

        Returns:
            float: вещественное число в диапазоне от 0 до 1,
            отражающее степень сходства строк
        """

        levenstein_distance: int = cls.estimate(first_line, second_line)

        similarity_score: float = 1 - levenstein_distance / max(len(first_line),
                                                                len(second_line))

        return similarity_score
