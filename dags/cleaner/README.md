# Cleaner
The Cleaner is use for many data lineage operations
- Cleaning text fields -> Removing unicode characters , coverting them to ASCII
- Converting text sates to datetime objects
- We can perform separate oprations on each field

Each outlet has their own cleaner class mentioned in the scraper config.
These classes can be instnatiated from the runCleaner.py . The run cleaner is the entry point of the cleaning stage of the pipeline
- Get all the results scraped by the scraper
- read the scraper config and get the cleaner for each outlet
- Use that outlets class to perform the cleaning

## Cleaner structure
All cleaner classes are in the cleaners.py file.
Example of cleaner:

```
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
```

The contructor collects all the articles belonging to that outlet and executes the cleaning methods for each field that needs cleaning

The results after the cleaning stage are stored in another json file. The data from this file is then written to the DB