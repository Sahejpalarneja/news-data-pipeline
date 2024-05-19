import config

if __name__ == '__main__':
    query = "SELECT * FROM public.articles;"
    conn = config.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    val = cursor.fetchall()
    print(val)