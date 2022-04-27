import pandas as pd
from bs4 import BeautifulSoup, Tag
from pandas import DataFrame
import requests
from time import sleep
from data import data
from random import randint
from typing import List

class Article:
    def __init__(self, title, authors, source, year, value, citations, link):
        self.title = title
        self.author = authors
        self.source = source
        self.year = year
        self.value = value
        self.citations = citations
        self.link = link

    def to_json(self):
        return json.dumps({
            "Название": self.title,
            "Авторы": self.author,
            "Журнал": self.source,
            "Год публикации": self.year,
            "Том": self.value,
            "Цитирования": self.citations,
            "Ссылка": self.link
        }, ensure_ascii=False, separators=(',', ': '))

    def __str__(self):
        return f"Название {self.title} Авторы {self.author} Журнал {self.source} Год {self.year} Том {self.value} Цитирования {self.citations} Ссылка {self.link}"

    def __repr__(self):
        return f"Название {self.title} Авторы {self.author} Журнал {self.source} Год {self.year} Том {self.value} Цитирования {self.citations} Ссылка {self.link}"

class Conf_Scraper:
    _soup: BeautifulSoup = None

    def __init__(self, text):
        self.html_text = text
        self._soup = BeautifulSoup(self.html_text, "lxml")

    def get_list_elements(self) -> List[Tag]:
        return self._soup.find("table", {"id": "restab"}).find_all("tr")[3:]

    @staticmethod
    def _get_title(td: Tag) -> str:
        data = td.find("b").text
        return data

    @staticmethod
    def _get_authors(td: Tag) -> str:
        try:
            data = td.find("i").text
        except AttributeError:
            data = "Авторы не указаны"
        return data

    @staticmethod
    def _get_source(td: Tag) -> str:
        try:
            data = td.find_all("font")[1].find_all("a")[0].text
        except IndexError:
            try:
                data = td.find_all("font")[1].text
                data = data.split("\n")[1].replace("\\xa", "")
            except IndexError:
                data = td.find_all("font")[0].text
        return data

    @staticmethod
    def _get_year(td: Tag) -> str:
        try:
            data = td.find_all("font")[1].text
            data_split = data.split("\n")[2]
        except IndexError:
            data_split = td.find_all("font")[0].text
        return data_split

    @staticmethod
    def _get_citations(td: Tag) -> str:
        return td.text.replace("\n", "")

    @staticmethod
    def _get_value(td: Tag) -> str:
        try:
            data = td.find_all("font")[1].text
            data_split = data.split("\n")[3].replace("\\xa0", "")
        except IndexError:
            data_split = td.find_all("font")[0].text
        return data_split
    @staticmethod
    def _get_link(td: Tag):   
        try:  
            data = 'https://www.elibrary.ru' + td.find_all('a')[0]['href']
        except IndexError:
            data = '-' 
        return data

    def _parse_td_elements(self, tr: Tag):
        get_center_td, *_ = tr.find_all("td")[1:]
        get_right_td = tr.find("td", "select-tr-right")
        title = self._get_title(get_center_td)
        authors = self._get_authors(get_center_td)
        source = self._get_source(get_center_td)
        year = self._get_year(get_center_td)
        value = self._get_value(get_center_td)
        citations = self._get_citations(get_right_td)
        link = self._get_link(get_center_td)
        return Article(title, authors, source, year, value, citations, link)

    @staticmethod
    def to_data_frame(list_articles: List[Article]) -> DataFrame:
        list_title = []
        list_authors = []
        list_source = []
        list_year = []
        list_value = []
        list_citations = []
        list_link = []
        for article in list_articles:
            list_title.append(article.title)
            list_authors.append(article.author)
            list_source.append(article.source)
            list_year.append(article.year)
            list_value.append(article.value)
            list_citations.append(article.citations)
            list_link.append(article.link)
        result_df = pd.DataFrame({
            "Название": list_title,
            "Авторы": list_authors,
            "Журнал": list_source,
            "Год": list_year,
            "Том": list_value,
            "Цитирования": list_citations,
            "Ссылка": list_link
        })
        return result_df

    def start(self) -> DataFrame:
        list_elements = self.get_list_elements()
        result_data = []
        for i in list_elements:
            result_data.append(self._parse_td_elements(i))
        return self.to_data_frame(result_data)
