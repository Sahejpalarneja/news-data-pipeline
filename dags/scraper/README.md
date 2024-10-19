# Scraper 

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


## Adding a new outlet to the Scraper
A new outlet to scrape can be easily added by just using a config
Example: 
```
"https://www.nbcnews.com/":{
        "articles": {
            "selector": ".storyline__headline > a",
            "withBaseName": true,
            "attribute": true
        },
        "attributes":{
            "title": {
                "selector": "head > title"
            },
            "text":{
                "selector": ".article-body__content > p",
                "distributed": true
            },
            "date":{
                "selector": "time",
                "attribute": "content"
            },
            "image":{
                "selector": "picture > img",
                "attribute": "src"
            },
            "author":{
                "selector":".byline-name"
            }
        },
        "cleaner": "NBCCleaner"
    },
```

- The key is the base link of the outlet: "https://www.nbcnews.com/"
- The "articles" key contains the information required scrape all the articles on the base outlet.
    - "selector" is the CSS base selector for all athe tags which contain the articles links
    - "withBaseName" tells if the the url needs the base name or not
    eg.
        "/article-title" Cannot be accessed, 
        "www.outlet.com/article-title" is the one which should be sraped
    - "attribute" flag set as true will enable the extarction to happen from within the html tag attributes
    eg.
        ```
        <a href="/article-title"></a>
        ```
        we need to get the href value.

- "attribute" key contains the information to scrape all the fields for each article
    - Each field will have a "selector" attribute necessary for getting the html tag
    - in addition to the "selector" the field can have "distributed" for fields which have the values in many child tags
    eg.
        ```
        <p>Some text</p>
        <p>Some more text</p>
        <p>Even more text</p>
        ```
        Here we need the the values from 3 tags
    - "attribute" key inside the field gives the name of the of the attribute in the html tag
    eg.
        ```
        <div content="Here is the text we need"></div>
        ```
- "cleaner" key is needed shows the name of the Cleaner class needed to clean the attributes