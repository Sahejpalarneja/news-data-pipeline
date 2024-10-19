import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(filename="dags/scraper/results/BaseScraper.log", level=logging.INFO)


class BaseScraper:

    def __init__(self, URL: str, config: str) -> None:
        self.URL = URL
        self.config = config
        headers: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
        }
        try:
            response = requests.get(URL, headers=headers)
            self._soup = BeautifulSoup(response.text, "html.parser")
        except Exception:
            logging.info(f"Could not set up Soup for {URL}")
        self.result: dict = self._setResult()
        self._functionMapping = {
        'title': 'getTitle',
        'text': 'getText',
        'date': 'getDate',
        'image': 'getImage',
        'author': 'getAuthor'
        }

    def getAttributes(self):
        attributes = self.config["attributes"]
        self.result["URL"] = self.URL
        for attribute, config in attributes.items():
            value = self.getAttributeFromSoup(attribute, config)
            self.result[attribute] = value


    def writeResults(self, articleResult: list) ->  list:
        articleResult.append(self.result)
        return articleResult


    def _setResult(self) -> dict:
        result: dict = {}
        result["URL"] = ""
        result["title"] = ""
        result["lead"] = ""
        result["author"] = ""
        result["date"] = ""
        result["text"] = ""
        result["image"] = ""
        return result


    def getAttributeFromSoup(self, name: str, attributeConfig: dict):
        functionName = self._functionMapping.get(name)
        function = getattr(self, functionName)
        return function(attributeConfig)


    def getTitle(self, attributeConfig: dict) -> str:
        selector = attributeConfig['selector']
        try:
            value = self._soup.select_one(selector).text
        except Exception:
            logging.info(f"Could not scrape title for {self.URL}")
            value = ''
        return value

    
    def getText(self, attributeConfig: dict) -> str:
        selector = attributeConfig['selector']
        if 'distributed' in attributeConfig.keys():
            try:
                tags = self._soup.select(selector)
                value = ''
                for p in tags:
                    value += p.text
            except Exception:
                logging.info(f"Could not scrape text for {self.URL}")
                value = ''
        else:
            value = self._soup.select_one(selector)
        return value


    def getDate(self, attributeConfig: dict) -> str:
        selector = attributeConfig['selector']
        try:
            tag = self._soup.select_one(selector)
            if 'attribute' in attributeConfig.keys():
                value = tag[attributeConfig['attribute']]
            else:
                value = tag
            #value = self.convertToDateTime(value)
        except Exception:
            logging.info(f"Could not scrape date for {self.URL}")
            value = ''
        return value
    

    def convertToDateTime(self, value) -> datetime:
        try:
            value = datetime.strptime(value[:-6], "%Y-%m-%dT%H:%M:%S")
        except Exception:
            logging.info(f'Could not convert to datetime for {self.URL}')
            pass
        return value
    

    def getImage(self, attributeConfig: dict) -> str:
        selector = attributeConfig['selector']
        try:
            value = self._soup.select_one(selector)
            if 'attribute' in attributeConfig.keys():
                value = value[attributeConfig['attribute']]
        except:
            logging.info(f"Could not scrape image for {self.URL}")
            value = ''
        return value
    

    def getAuthor(self, attributeConfig: dict) -> str:
        selector = attributeConfig['selector']
        try:
            value = self._soup.select_one(selector).text
            if 'attribute' in attributeConfig.keys():
                value = value[attributeConfig['attribute']]
        except:
            logging.info(f"Could not scrape Author for {self.URL}")
            value = ''
        return value
