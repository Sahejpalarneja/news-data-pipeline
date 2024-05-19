import requests
from bs4 import BeautifulSoup
import json


class BaseScraper:
    def __init__(self, URL: str, config: str) -> None:
        self.URL = URL
        self.config = config
        headers: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
        }
        response = requests.get(URL, headers=headers)
        self._soup = BeautifulSoup(response.text, "html.parser")
        self.result: dict = self._setResult()

    def getAttributes(self):
        attributes = self.config["attributes"]
        self.result["URL"] = self.URL
        for attribute in attributes.keys():
            selector = attributes[attribute]
            value = self._soup.select_one(selector).text
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
