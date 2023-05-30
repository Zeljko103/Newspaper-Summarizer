import re
import tkinter
from typing import Optional, List

import newspaper
from newspaper import Article
from textblob import TextBlob


class MojClanak:
    __MAPIRANA_AZBUKA = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ђ": "đ", "е": "e", "ж": "ž", "з": "z",
                         "и": "i", "ј": "j", "к": "k", "л": "l", "љ": "lj", "м": "m", "н": "n", "њ": "nj", "о": "o",
                         "п": "p", "р": "r", "с": "s", "т": "t", "ћ": "ć", "у": "u", "ф": "f", "х": "h", "ц": "c",
                         "ч": "č", "џ": "dž", "ш": "š", "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Ђ": "Đ",
                         "Е": "E", "Ж": "Ž", "З": "Z", "И": "I", "Ј": "J", "К": "K", "Л": "L", "Љ": "Lj", "М": "M",
                         "Н": "N", "Њ": "Nj", "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T", "Ћ": "Ć", "У": "U",
                         "Ф": "F", "Х": "H", "Ц": "C", "Ч": "Č", "Џ": "Dž", "Ш": "Š"}

    def __init__(self):
        self.__moj_clanak: Optional[Article] = None
        self.__vise_clanaka: tkinter.BooleanVar = tkinter.BooleanVar()
        self.__analiza: Optional[TextBlob] = None

    @property
    def vise_clanaka(self) -> tkinter.BooleanVar:
        return self.__vise_clanaka

    def set_vise_clanaka(self, vs_clnk: bool) -> None:
        self.__vise_clanaka.set(vs_clnk)

    @property
    def moj_clanak(self) -> Optional[Article]:
        return self.__moj_clanak

    def set_moj_clanak(self, moj_clnk: Article) -> None:
        self.__moj_clanak = moj_clnk

    @property
    def analiza(self) -> Optional[TextBlob]:
        return self.__analiza

    def set_analiza(self, anlz: TextBlob) -> None:
        self.__analiza = anlz

    def obrada(self, url: str) -> None:

        if self.__vise_clanaka.get():
            self.obrada_vise_clanaka(url)
            return
        self.__moj_clanak = Article(url)
        self.__moj_clanak.download()
        if self.__cirilica():
            self.__moj_clanak.set_html(MojClanak.transkripcija(self.__moj_clanak.html))
        self.__moj_clanak.parse()
        self.__moj_clanak.nlp()
        self.__analiza = TextBlob(self.__moj_clanak.text)

    def __cirilica(self) -> bool:
        if self.__moj_clanak is not None:
            return any(char in MojClanak.__MAPIRANA_AZBUKA.keys() for char in self.__moj_clanak.html)
        return False

    @staticmethod
    def obrada_vise_clanaka(url: str) -> List[str]:
        return [article.url for article in newspaper.build(url).articles]

    @staticmethod
    def transkripcija(text: str) -> str:
        return "".join(
            MojClanak.__MAPIRANA_AZBUKA[char] if char in MojClanak.__MAPIRANA_AZBUKA.keys() else char for char in text)

    @staticmethod
    def validan_url(string):
        url_pattern = re.compile(r"^(http|https)://", re.IGNORECASE)
        return re.match(url_pattern, string) is not None
