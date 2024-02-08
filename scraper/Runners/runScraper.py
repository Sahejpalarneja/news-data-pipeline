import json
import requests
from BaseScraper.BaseScraper import BaseScraper
from urllib.parse import urljoin
from bs4 import BeautifulSoup


configPath: str = 'scraper\config\scraperConfig.json'
configHandle = open(configPath, 'r').read()
config: dict =  json.loads(configHandle)


def getAllArticles(Outletscraper: BaseScraper) -> list: #TODO maybe method can be moved to the base class
    articles: list = Outletscraper._soup.select(Outletscraper.config['articles']['selector'])
    if Outletscraper.config['articles']['attribute']:
        if Outletscraper.config['articles']['withBaseName']:
            articles = [a['href'] for a in articles]
        else:
            articles = [urljoin(Outletscraper.URL, a['href']) for a in articles]
    # TODO add condition if no href but basename 
    return articles


def parseArticles(config, articles): #TODO Maybe method can be moved to the base class
    with open("scraper/results/scraperResults.json", "r") as resultHandle:
        try:
            articleResult = json.load(resultHandle)
        except ValueError:
            articleResult = []
        count = 0
        for article in articles:
            articleScraper = BaseScraper(article, config)
            articleScraper.getAttributes()
            articleScraper.writeResults(articleResult)
            count += 1
            print(f"{count}/{len(articles)} articles scraped for {articleScraper.URL}")
    with open("scraper/results/scraperResults.json", "w") as resultHandle:
        resultHandle.write(json.dumps(articleResult, indent= 4))


if __name__ == '__main__':
    for url, config in config.items():
        Outletscraper = BaseScraper(url, config)
        articles: list = getAllArticles(Outletscraper)
        parseArticles(config, articles)
    