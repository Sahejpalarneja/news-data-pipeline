import config
import json

resultPath: str  = './cleaner/results/cleanedResults.json'
resultHandle = open(resultPath, 'r', encoding='utf-8')
results : dict = json.load(resultHandle)

def getAllArticlesTitles(cursor) -> list:
    query = "SELECT title FROM articles"
    cursor.execute(query)
    return [x[0] for x in cursor.fetchall()]


def createQuery(article: dict) -> str:
    query = "INSERT INTO public.articles("
    for k,v in article.items():
        if article[k] != '':
            query += k + ','
    query = query[:-1] +') VALUES ('
    for k,v in article.items():
        if article[k] != '':
            query += "'"+article[k]+"',"
    query = query[:-1] + ');'
    return query


def addArticle(article: dict, cursor) -> None:
    query = createQuery(article)
    cursor.execute(query)

if __name__ == '__main__':
    with config.connect() as conn:
        cursor = conn.cursor()
        allTitles = getAllArticlesTitles(cursor)
        for article in results:
            if article['title']  not in allTitles:
                addArticle(article, cursor)
                conn.commit()

    