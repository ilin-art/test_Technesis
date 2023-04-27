import sqlite3
import pandas as pd


def save_to_sqlite(file_path):
    # Прочитать файл Excel и сохранить его содержимое в DataFrame
    df = pd.read_excel(file_path)

    # Открыть соединение с базой данных sqlite
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Создать таблицу 'sites', если она не существует
    c.execute('''CREATE TABLE IF NOT EXISTS sites
                 (title text, url text, xpath text)''')

    # Добавить данные в таблицу
    for index, row in df.iterrows():
        title = row['title']
        url = row['url']
        xpath = row['xpath']
        c.execute("INSERT INTO sites (title, url, xpath) VALUES (?, ?, ?)",
                  (title, url, xpath))

    # Сохранить изменения и закрыть соединение с базой данных
    conn.commit()
    conn.close()
