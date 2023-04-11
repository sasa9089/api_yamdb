import sqlite3
import csv

# открываем соединение с базой данных
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# открываем файл CSV и считываем данные
with open('D:/Dev/api_yamdb/api_yamdb/static/data/genre.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    # проходим по строкам CSV и добавляем данные в базу данных
    for row in reader:
        cursor.execute("INSERT INTO reviews_genre (id, name, slug) VALUES (?, ?, ?)",
                       (row['id'], row['name'], row['slug']))

# сохраняем изменения и закрываем соединение
conn.commit()
conn.close()