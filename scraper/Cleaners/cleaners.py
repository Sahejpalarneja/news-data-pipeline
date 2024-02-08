class BBCCleaner:

    def __init__(self, resultConfig, url) -> None:
        self.baseURL = url
        self.articles = [a for a in resultConfig if a["URL"].startswith(self.baseURL)]
    
    def clean(self) -> None:
        for article in self.articles:
            article['title'] = self._cleanTitle(article['title'])
        return self.articles

    def _cleanTitle(self, title: str) -> str:
        try:
            title = ''.join(title.split('-')[:-1])
        except:
            return title
        return title
    