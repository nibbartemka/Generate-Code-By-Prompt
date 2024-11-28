from typing import List, Optional

from lexer import (Lexer, LevensteinSimilarityEstimator,
                   Lexem, LexemInfo)
from prompts import (Prompt, SaveNumbersFromList, RemoveNumbersFromList,
                     FindAllTagsFromSite, ReadFilesMultithreading)

MIN_SIMILARITY_COEFFICIENT: float = 0.5


def get_prompt_similarity(user_lexem_info: List[LexemInfo], 
                          prompt_lexem_info: List[LexemInfo]) -> float:
    return (len([lexem_info
                 for lexem_info in user_lexem_info
                 if lexem_info in prompt_lexem_info])
            / len(prompt_lexem_info))


if __name__ == '__main__':
    user_inquiry: str = 'оставить в случайном списке числа от 2 до 5'.lower()

    lexer: Lexer = Lexer(user_inquiry,
                         LevensteinSimilarityEstimator)

    user_lexem: List[Lexem] = lexer.get_all_lexem()
    user_lexem_info: List[LexemInfo] = [lexem.lexem_info for lexem in user_lexem]

    prompt_classes: List[Prompt] = [SaveNumbersFromList,
                                    RemoveNumbersFromList,
                                    FindAllTagsFromSite,
                                    ReadFilesMultithreading]

    max_prompt_similarity: float = 0.0
    suitable_prompt_class: Optional[Prompt] = None

    for prompt_class in prompt_classes:
        prompt_lexem_info: List[LexemInfo] = prompt_class.get_lexem_info()
        prompt_similarity: float = get_prompt_similarity(user_lexem_info,
                                                         prompt_lexem_info)
        if prompt_similarity > max_prompt_similarity:
            suitable_prompt_class = prompt_class
            max_prompt_similarity = prompt_similarity

    if max_prompt_similarity > MIN_SIMILARITY_COEFFICIENT:
        prompt: Prompt = suitable_prompt_class(user_lexem)

        print('PYTHON', prompt.to_python(), sep='\n')
        print()
        print('JAVA', prompt.to_java(), sep='\n')
    else:
        print('Упс... что-то пошло не так!')
