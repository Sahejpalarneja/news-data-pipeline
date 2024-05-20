import logging

logging.basicConfig(filename="cleaner/results/BaseCleaner.log", level=logging.INFO)

class NewsWeekCleaner:

    def __init__(self, resultConfig, url) -> None:
        self.baseURL = url
        self.articles = [a for a in resultConfig if a["URL"].startswith(self.baseURL)]
    
    def clean(self) -> None:
        for article in self.articles:
            article['title'] = self._cleanTitle(article['title'])
            article['text'] = self._cleanText(article['text'])
        return self.articles

    def _cleanTitle(self, title: str) -> str:
        try:
            title = title.encode('latin-1').decode('unicode-escape')
        except Exception:
            logging.info(f"Could not clean title for {self.baseURL}")
        return title


    def _cleanText(self, text: str) -> str:
        try:
            text = text.encode('latin-1').decode('unicode-escape')
        except Exception:
            logging.info(f"Could not clean text for {self.baseURL}")
        return text
    