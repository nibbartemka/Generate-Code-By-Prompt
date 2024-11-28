from typing import List, Dict
import random

from .prompt import Prompt
from lexer import LexemInfo, Lexem


class RemoveNumbersFromList(Prompt):
    lexem_info: List[LexemInfo] = [
        LexemInfo.FILTER_REMOVE,
        LexemInfo.LIST,
        LexemInfo.FROM,
        LexemInfo.INTEGER,
        LexemInfo.TO,
        LexemInfo.INTEGER,
    ]

    def __init__(self, all_lexem: List[Lexem]) -> None:
        data_dict: Dict[str, str] = self.__preprocess_data(all_lexem)

        self.list_arg = data_dict['list_arg']
        self.min_number = data_dict['min_number']
        self.max_number = data_dict['max_number']

    def __preprocess_data(self, all_lexem: List[Lexem]) -> Dict[str, str]:
        list_arg = [lexem.value
                    for lexem in all_lexem
                    if lexem.lexem_info == LexemInfo.LIST]
        list_arg.extend([None])

        border_numbers = [lexem.value
                          for lexem in all_lexem
                          if lexem.lexem_info == LexemInfo.INTEGER]
        border_numbers.extend([None, None])

        min_number, max_number, *_ = border_numbers
        list_arg, *_ = list_arg

        if not min_number:
            min_number = random.randint(1, 100)

        if not max_number:
            max_number = random.randint(int(min_number) + 1,
                                        int(min_number) + 20)

        if not list_arg:
            numbers = [random.randint(int(min_number) - 10,
                                      int(min_number) + 30)
                       for _ in range(random.randint(5, 10))]
            list_arg = numbers

        return {
            'list_arg': list_arg,
            'min_number': min_number,
            'max_number': max_number,
        }

    @classmethod
    def get_lexem_info(cls) -> List[LexemInfo]:
        return cls.lexem_info

    def to_python(self) -> str:
        return f"""
            nums = {self.list_arg}
            filtered_nums = [num
                             for num in nums
                             if {self.min_number} > num or num > {self.max_number}]
            print(filtered_nums)
        """

    def to_java(self) -> str:
        return f"""
            import java.util.Arrays;
            import java.util.List;
            import java.util.stream.Collectors;

            public class Main {{
                public static void main(String[] args) {{
                    List<Integer> numbers = Arrays.asList({self.list_arg});

                    int min = {self.min_number};
                    int max = {self.max_number};

                    List<Integer> filteredNumbers = numbers.stream()
                            .filter(num -> num < min || num > max)
                            .collect(Collectors.toList());

                    System.out.println(filteredNumbers);
                }}
            }}
        """
