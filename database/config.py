from configparser import ConfigParser
import os
import psycopg2


def load_config(filename: str='database\database.ini', section:str='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    
    config: dict = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = parser.get(section, param[1], vars=os.environ)
    return config

def connect():
    config = load_config()
    config['password'] = config['password'].split('"')[1]
    cnx = psycopg2.connect(user=config['user'], password=config['password'], host="news-data-pipline.postgres.database.azure.com", port=5432, database="postgres")
    return cnx

    