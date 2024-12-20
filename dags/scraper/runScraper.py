import json
import logging

logging.basicConfig(filename="dags/scraper/results/RunScraper.log", level=logging.INFO, filemode = "w+")

from scraper.BaseScraper.BaseScraper import BaseScraper
from urllib.parse import urljoin

configPath: str = 'dags/scraper/config/scraperConfig.json'


def getAllArticles(Outletscraper: BaseScraper) -> list: #TODO maybe method can be moved to the base class
    """Gets all the urls for the articles on the Base URL
    Args:
        OutletScraper: BaseScraper object which has the soup of the base URL
    Returns:
        list of the urls of all the articles in the base URL"""
    articles: list = Outletscraper._soup.select(Outletscraper.config['articles']['selector'])
    if Outletscraper.config['articles']['attribute']:
        if Outletscraper.config['articles']['withBaseName']:
            articles = [a['href'] for a in articles] #if the url is in the arrtibutes of the html element
        else:
            articles = [urljoin(Outletscraper.URL, a['href']) for a in articles] #if the url needs the base url as a prefix
    logging.info(f"Found {len(set(articles))} for {Outletscraper.URL}")
    # TODO add condition if no href but basename 
    return set(articles)


def parseArticles(config: dict, articles: set): #TODO Maybe method can be moved to the base class
    """Parses all articles based on the config of the base URL
    Args:
        config: dict of the config for the base URL
        articles: list of the urls for the articles in the base URL"""
    try:
        resultHandle = open("dags/scraper/results/scraperResults.json", "r")
        try:
            articleResult = json.load(resultHandle)
        except Exception:
            articleResult = []
    except FileNotFoundError:
        articleResult = []
    count = 0
    for article in articles:
        articleScraper = BaseScraper(article, config)
        articleScraper.getAttributes() #Scrape all the available attributes from the article
        articleScraper.writeResults(articleResult)
        count += 1
        logging.info(f"{count}/{len(articles)} articles scraped for {articleScraper.URL}")
    with open("dags/scraper/results/scraperResults.json", "w") as resultHandle:
        resultHandle.write(json.dumps(articleResult, indent= 4)) #Writing results for 1 base URL


def runScraper():
    config: dict =  json.loads(open(configPath, 'r').read())
    for url, config in config.items():
        Outletscraper = BaseScraper(url, config)
        articles: set = getAllArticles(Outletscraper)
        parseArticles(config, articles)
        logging.info("Scraping finished")
    