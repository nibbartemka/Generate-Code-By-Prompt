from typing import List, Dict

from .prompt import Prompt
from lexer import LexemInfo, Lexem


class FindAllTagsFromSite(Prompt):
    lexem_info: List[LexemInfo] = [
        LexemInfo.URL,
        LexemInfo.HTML_TAG,
        LexemInfo.SEARCH,
    ]

    def __init__(self, all_lexem: List[Lexem]) -> None:
        data_dict: Dict[str, str] = self.__preprocess_data(all_lexem)

        self.url = data_dict['url_arg']
        self.tag = data_dict['searching_tag']

    def __preprocess_data(self, all_lexem: List[Lexem]) -> Dict[str, str]:
        url = [lexem.value
               for lexem in all_lexem
               if lexem.lexem_info == LexemInfo.URL]
        url.extend([None])

        tag = [lexem.value
               for lexem in all_lexem
               if lexem.lexem_info == LexemInfo.HTML_TAG]
        tag.extend([None])

        searching_tag, *_ = tag
        url_arg, *_ = url

        if not searching_tag:
            searching_tag = 'div'

        if not url_arg:
            url_arg = 'https://www.example.com'

        return {
            'searching_tag': searching_tag,
            'url_arg': url_arg,
        }

    @classmethod
    def get_lexem_info(cls) -> List[LexemInfo]:
        return cls.lexem_info

    def to_python(self) -> str:
        return f"""
            import requests
            from bs4 import BeautifulSoup

            url = "{self.url}"

            try:
                response = requests.get(url)

                soup = BeautifulSoup(response.text, 'html.parser')
                tags = soup.find_all("{self.tag}")
                for tag in tags:
                    print(tag.text)
            except Exception as error:
                print(f"Ошибка при получении страницы: {{error}}")
        """

    def to_java(self) -> str:
        return f"""
            import org.jsoup.Jsoup;
            import org.jsoup.nodes.Document;
            import org.jsoup.nodes.Element;
            import org.jsoup.select.Elements;

            import java.io.IOException;

            public class Main {{
                public static void main(String[] args) {{
                    String url = "{self.url}";

                    try {{
                        Document doc = Jsoup.connect(url).get();

                        Elements tags = doc.select("{self.tag}");

                        for (Element tag : tags) {{
                            System.out.println(tag.text());
                        }}
                    }} catch (IOException e) {{
                        e.printStackTrace();
                    }}
                }}
            }}
        """
