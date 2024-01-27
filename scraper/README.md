## Scraper 

The Scraper is written in Python using the following libraries
- requests
- BeautifulSoup

We have a BaseScraper which sets up the basics of the requests and the html parser gets the information from the websites. 
The BaseScraper has the header information of the headers if any website requires it for the response 

## Information to be Scraped
The scraper will get the following information from a website:
- title
- tags
- lead
- author
- date published
- text
- image link 