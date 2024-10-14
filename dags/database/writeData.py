import config
import json
import logging

logging.basicConfig(filename="dags/database/writer.log", level=logging.INFO, filemode = "w+")
resultPath: str  = 'dags/cleaner/results/cleanedResults.json'


def getAllArticlesTitles(cursor) -> list:
    """Gets the tiltes of all the currently present articles
    Args:
        cursor: The cursor for the DB to query
    Returns:
        list of all the titles
    """
    query = "SELECT title FROM articles"
    cursor.execute(query)
    return [x[0] for x in cursor.fetchall()]


def createQuery(article: dict) -> str:
    """Creates the query for the articles, all values might not be present for all the articles
    Args:
        articles: dictionary of the article
    Returns:
        query: query for the present values
    """
    query = "INSERT INTO public.articles("
    for k,v in article.items(): #TODO remove value if not in use
        if article[k] != '':
            query += k + ','
    query = query[:-1] +') VALUES ('
    for k,v in article.items():
        if article[k] != '':
            query += "'"+article[k]+"',"
    query = query[:-1] + ');'
    return query


def addArticle(article: dict, cursor, local_json_file: bool = False) -> None: #TODO function is useless at he moment
    """Executes the query """
    query = createQuery(article)
    if local_json_file:
        return query
    else:
        cursor.execute(query)

if __name__ == '__main__':
    """
    Starting point of the writer
    """
    results : dict = json.load(open(resultPath, 'r', encoding='utf-8'))
    local_check = None
    #local_check = open('dags/database/local_check.txt', 'a+') 

    with config.connect() as conn:
        cursor = conn.cursor()
        allTitles = getAllArticlesTitles(cursor)
        count = 0
        for article in results:
            if article['title'] not in allTitles: #check if the article is already present from the past
                #TODO Better way to differentiate between already written articles
                try:
                    if local_check is None:
                        addArticle(article, cursor)
                    else:
                        line = addArticle(article, cursor, True)
                        local_check.write(line+'\n\n')
                    count += 1
                except Exception as ex:
                    logging.warning(f"Could not add article to the DB: {article['title']}")
                    logging.warning(f"Error was {ex}")
            else:
                logging.info(f"Article already in the DB, title: {article['title']}")
            if local_check is None:
                conn.commit()
        logging.info(f"Added {count} articles to the DB")
    