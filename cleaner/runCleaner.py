import json
import cleaners
import logging

logging.basicConfig(filename="cleaner/results/Cleaner.log", level=logging.INFO)

configPath: str = '././scraper/config/scraperConfig.json'
configHandle = open(configPath, 'r')
config: dict =  json.load(configHandle)

resultPath: str  = '././scraper/results/scraperResults.json'
resultHandle = open(resultPath, 'r')
results : dict = json.load(resultHandle)

cleanedResultsPath: str = "cleaner/results/cleanedResults.json"

def updateArticles(cleaneadArticles: list) -> None:
    with open(cleanedResultsPath, 'w', encoding='ascii') as fhandle:
        fhandle.write(json.dumps(cleaneadArticles, indent=4))


if __name__ == '__main__':
    cleanedArticles = []
    for url, config in config.items():
        try:
            if 'cleaner' in config.keys():
                cl = getattr(cleaners, config['cleaner'])(results, url)
                cleanedArticles += cl.clean()
            else:
                cleanedArticles += [a for a in results if a["URL"].startswith(url)]
                logging.info(f"No Cleaner for {url}")
                
        except KeyError:
            print("No cleaner for this Scraper")
    updateArticles(cleanedArticles)
       
        