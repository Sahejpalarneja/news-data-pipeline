import logging
import re
import unicodedata
import unidecode

logging.basicConfig(filename="dags/cleaner/results/BaseCleaner.log", level=logging.INFO, filemode = "w+")


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = unidecode.unidecode(text)
    text = re.sub('"', ' ', text)
    text = re.sub("'", ' ', text)
    return text

class NBCCleaner:
    def __init__(self, resultConfig, url) -> None:
        self.baseURL = url
        self.articles = [a for a in resultConfig if a["URL"].startswith(self.baseURL)]
    
    def clean(self) -> None:
        for article in self.articles:
            article['title'] = self._cleanTitle(article['title'])
            article['text'] = self._cleanText(article['text'])
            article['date'] = self._cleanDate(article['date'])
            logging.info(f"Cleaned Article. {article['URL']}")
        return self.articles

    def _cleanTitle(self, title: str) -> str:
        try:
            title = normalize_text(title)
        except Exception:
            logging.warning(f"Could not clean title for {self.baseURL}")
        return title

    def _cleanText(self, text: str) -> str:
        try:
            text = normalize_text(text)
        except Exception:
            logging.warning(f"Could not clean text for {self.baseURL}")
        return text
    
    def _cleanDate(self, date: str) -> str:
        try:
            date = date.split('T')[0]
        except:
            logging.warning(f"Could not clean date for {self.baseURL}")
        return date

    
    
class NewsWeekCleaner:

    def __init__(self, resultConfig, url) -> None:
        self.baseURL = url
        self.articles = [a for a in resultConfig if a["URL"].startswith(self.baseURL)]
    
    def clean(self) -> None:
        for article in self.articles:
            article['title'] = self._cleanTitle(article['title'])
            article['text'] = self._cleanText(article['text'])
            article['date'] = self._cleanDate(article['date'])
            article['author'] = self._cleanAuthor(article['author'])
            logging.info(f"Cleaned Article. {article['URL']}")
        return self.articles

    def _cleanTitle(self, title: str) -> str:
        try:
            title = normalize_text(title)
        except Exception:
            logging.warning(f"Could not clean title for {self.baseURL}")
        return title

    def _cleanText(self, text: str) -> str:
        try:
            text = normalize_text(text)
        except Exception:
            logging.warning(f"Could not clean text for {self.baseURL}")
        return text

    def _cleanDate(self, date: str) -> str:
        try:
            date = date.split('T')[0]
        except:
            logging.warning(f"Could not clean date for {self.baseURL}")
        return date
    
    def _cleanAuthor(self, author: str) -> str:
        try:
            author = normalize_text(author)
        except:
            logging.warning(f"Could not clean author for {self.baseURL}")
        return author
