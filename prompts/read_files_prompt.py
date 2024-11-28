from typing import List, Dict

from .prompt import Prompt
from lexer import LexemInfo, Lexem


class ReadFilesMultithreading(Prompt):
    lexem_info: List[LexemInfo] = [
        LexemInfo.READ,
        LexemInfo.FILE,
        LexemInfo.MULTITHREADING,
    ]

    def __init__(self, all_lexem: List[Lexem]) -> None:
        data_dict: Dict[str, str] = self.__preprocess_data(all_lexem)

        self.files = data_dict['files']

    def __preprocess_data(self, all_lexem: List[Lexem]) -> Dict[str, str]:
        files = [lexem.value
                 for lexem in all_lexem
                 if lexem.lexem_info == LexemInfo.FILE]

        if not files:
            files.extend(['example1.txt',
                          'example2.txt',
                          'example3.txt'])
        return {
            'files': files,
        }

    @classmethod
    def get_lexem_info(cls) -> List[LexemInfo]:
        return cls.lexem_info

    def to_python(self) -> str:
        return f"""
            from concurrent.futures import (ThreadPoolExecutor,
                                            as_completed)

            def read_file(file_name):
                try:
                    with open(file_name, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                        return file_content
                except Exception as e:
                    return f"Ошибка при чтении файла {{file_name}}"

            file_names = {self.files}
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(read_file, file_name)
                        for file_name in file_names]

                for future in as_completed(futures):
                    result = future.result()
                    print(result)
        """

    def to_java(self) -> str:
        return f"""
            import java.io.BufferedReader;
            import java.io.FileReader;
            import java.util.concurrent.ExecutorService;
            import java.util.concurrent.Executors;

            public class Program {{

                public static void main(String[] args) {{
                    String[] files = {{ {', '.join(self.files)} }};
                    ExecutorService executor = Executors.newFixedThreadPool(files.length);

                    for (String file : files) {{
                        executor.submit(() -> readFile(file));
                    }}

                    executor.shutdown();
                }}

                private static void readFile(String fileName) {{
                    try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {{
                        String line;
                        while ((line = br.readLine()) != null) {{
                            System.out.println(line);
                        }}
                    }} catch (IOException e) {{
                        System.out.println("Ошибка при чтении файла " + fileName);
                    }}
                }}
            }}
        """
