import json
import sys
from Cleaners import cleaners


configPath: str = 'scraper\config\scraperConfig.json'
configHandle = open(configPath, 'r')
config: dict =  json.load(configHandle)

resultPath: str  = 'scraper\\results\\scraperResults.json'
resultHandle = open(resultPath, 'r')
results : dict = json.load(resultHandle)


def updateArticles(cleaneadArticles: list) -> None:
    with open(resultPath, 'w') as fhandle:
        fhandle.write(json.dumps(results, indent=4))


if __name__ == '__main__':
    for url, config in config.items():
        try:
            cl = getattr(cleaners, config['cleaner'])(results, url)
            cleanedArticles = cl.clean()
            updateArticles(cleanedArticles)
            
        except KeyError:
            print("No cleaner for this cleaner")
       
        