""" Propmpts

Данный пакет предоставляет промпты, по которым в дальнейшем будет
сгенерирован код на двух языках: Python и Java

Modules:
- prompt: модуль, в котором объявляется абстрактный класс промпта.
- find_all_tags_prompt: модуль, в котором определен промпт для генерации кода
парсера сайта и поиска всех вхождений некоторого тега.
- read_files_prompt: модуль, в котором определен промпт
для многопоточного чтения файлов.
- save_nums_prompt: модуль, в котором определен промпт для фильтрации списка чисел, 
исходя из указанного минимума и максимума. Числа, попадающие в диапазон, остаются в списке.
- remove_nums_prompt: модуль, в котором определен промпт для фильтрации списка чисел, 
исходя из указанного минимума и максимума. Числа, попадающие в диапазон, убираются из списка.
"""


from .prompt import Prompt
from .save_nums_prompt import SaveNumbersFromList
from .remove_nums_prompt import RemoveNumbersFromList
from .find_all_tags_prompt import FindAllTagsFromSite
from .read_files_prompt import ReadFilesMultithreading
