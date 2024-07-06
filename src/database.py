import sqlite3


def init_db():
    conn = sqlite3.connect('job_search.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_search (
            id INTEGER PRIMARY KEY,
            city TEXT,
            job TEXT,
            min_salary INTEGER,
            max_salary INTEGER,
            url TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_job_search_to_db(city, job, min_salary, max_salary, url):
    conn = sqlite3.connect('job_search.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO job_search (city, job, min_salary, max_salary, url)
        VALUES (?, ?, ?, ?, ?)
    ''', (city, job, min_salary, max_salary, url))
    conn.commit()
    conn.close()


# Функция для проверки наличия URL в базе данных
def check_if_url_exists(url):
    conn = sqlite3.connect('job_search.db')
    cursor = conn.cursor()
    # Подготавливаем SQL-запрос для поиска URL
    query = "SELECT * FROM job_search WHERE url = ?"
    cursor.execute(query, (url,))

    # Получаем результат
    result = cursor.fetchone()

    # Закрываем соединение с базой данных
    conn.close()

    # Если результат не None, значит URL найден
    if result is None:
        return False
    return True
