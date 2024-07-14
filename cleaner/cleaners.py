import logging
import re

logging.basicConfig(filename="cleaner/results/BaseCleaner.log", level=logging.INFO, filemode = "w+")


class NBCCleaner:
    def __init__(self, resultConfig, url) -> None:
        self.baseURL = url
        self.articles = [a for a in resultConfig if a["URL"].startswith(self.baseURL)]
    
    def clean(self) -> None:
        for article in self.articles:
            article['title'] = self._cleanTitle(article['title'])
            article['text'] = self._cleanText(article['text'])
            article['date'] = self._cleanDate(article['date'])
        return self.articles


    def _cleanTitle(self, title: str) -> str:
        try:
            title = re.sub('"', ' ', title)
            title = re.sub("'", ' ', title)
            title = re.sub("”", ' ', title)
        except Exception:
            logging.warn(f"Could not clean title for {self.baseURL}")
        return title


    def _cleanText(self, text: str) -> str:
        try:
            text = re.sub('"', ' ', text)
            text = re.sub("'", ' ', text)
            text = re.sub("”", ' ', text)
        except Exception:
            logging.warn(f"Could not clean text for {self.baseURL}")
        return text
    
    def _cleanDate(self, date: str) -> str:
        try:
            date = date.split('T')[0]
        except:
            logging.warn(f"Could not clean date for {self.baseURL}")
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
        return self.articles


    def _cleanTitle(self, title: str) -> str:
        try:
            title = re.sub('"', ' ', title)
            title = re.sub("'", ' ', title)
            title = re.sub("”", ' ', title)
            
        except Exception:
            logging.warn(f"Could not clean title for {self.baseURL}")
        return title


    def _cleanText(self, text: str) -> str:
        try:
            text = re.sub('"', ' ', text)
            text = re.sub("'", ' ', text)
            text = re.sub("”", ' ', text)
        except Exception:
            logging.warn(f"Could not clean text for {self.baseURL}")
        return text

    def _cleanDate(self, date: str) -> str:
        try:
            date = date.split('T')[0]
        except:
            logging.warn(f"Could not clean date for {self.baseURL}")
        return date