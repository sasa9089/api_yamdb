# Проект YaMDb
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Технологии:
+ Python3  
+ Django
+ Django REST Framework 

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/sasa9089/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Если есть необходимость, заполняем базу тестовыми данными:

Запускаем терминал Sqlite:

```
новый терминал -> Command prompt(cmd)
```

```
sqlite3 db.sqlite3
```

Выбираем формат csv:

```
.mode csv
```
```
.import --csv путь_к_файлу_с_данными_для_таблицы/файл.csv имя_приложения_имя_таблицы
```

Проверяем наполнилась ли БД:

```
SELECT * FROM имя_таблицы;
```

## После запуска проекта, доступна документация для API Yamdb: 
### http://127.0.0.1:8000/redoc/
В документации описаны доступные адреса и команды.
Документация представлена в формате Redoc.

# Примеры запросов

## Алгоритм регистрации пользователей

**POST** ```/api/v1/auth/signup/```
```
{
  "email": "string",
  "username": "string"
}
```

Получение JWT-токена:

**POST** ```/api/v1/auth/token/```

```
{
  "username": "string",
  "confirmation_code": "string"
}
```

## Категории (типы) произведений

Получить список всех категорий:

**GET** ```/api/v1/categories/```

Добавление новой категории:

**POST** ```/api/v1/categories/```
```
{
  "name": "string",
  "slug": "string"
}
```
Удаление категории:

**DELETE** ```/api/v1/categories/{slug}/```


## Жанры произведений

Получить список всех жанров:

**GET** ```/api/v1/genres/```

Добавление жанра:

**POST** ```/api/v1/genres/```
```
{
  "name": "string",
  "slug": "string"
}
```
Удаление жанра:

**DELETE** ```/api/v1/genres/{slug}/```

## Произведения, к которым пишут отзывы (определённый фильм, книга или песенка)

Получение списка всех произведений:

**GET** ```/api/v1/titles/```

Добавление произведения:

**POST** ```/api/v1/titles/```
```
{
  "name": "string",
  "year": "integer",
  "description(optional)": "string ",
  "genre": "Array of strings",
  "category": "string "
}
```

Получение информации о произведении:

**GET** ```/api/v1/titles/{titles_id}/```

Частичное обновление информации о произведении:

**PATCH** ```/api/v1/titles/{titles_id}/```
```
{
  "name": "string",
  "year": "integer",
  "description(optional)": "string ",
  "genre": "Array of strings",
  "category": "string "
}
```

Удаление произведения:

**DELETE** ```/api/v1/titles/{titles_id}/```

## Отзывы

Получение списка всех отзывов:

**GET** ```/api/v1/titles/{title_id}/reviews/```

Добавление нового отзыва:

**POST** ```/api/v1/titles/{title_id}/reviews/```
```
{
  "text": "string",
  "score": "integer"
}
```

Получить отзыв по id для указанного произведения:

**GET** ```/api/v1/titles/{title_id}/reviews/{review_id}/```

Частичное обновление отзыва по id:

**PATCH** ```/api/v1/titles/{title_id}/reviews/{review_id}/```
```
{
  "text": "string",
  "score": "integer"
}
```

Удаление отзыва по id:

**DELETE** ```/api/v1/titles/{title_id}/reviews/{review_id}/```

## Комментарии к отзывам

Получение списка всех комментариев к отзыву:

**GET** ```/api/v1/titles/{title_id}/reviews/{review_id}/comments/```

Добавление комментария к отзыву:

**POST** ```/api/v1/titles/{title_id}/reviews/{review_id}/comments/```
```
{
  "text": "string"
}
```

Получение комментария к отзыву:

**GET** ```/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```

Частичное обновление комментария к отзыву:

**PATCH** ```/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```
```
{
  "text": "string"
}
```

Удаление комментария к отзыву:

**DELETE** ```/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```

## Пользователи

Получение списка всех пользователей:

**GET** ```/api/v1/users/```

Добавление пользователя:

**POST** ```/api/v1/users/```
```
{
  "username": "string",
  "email": "string <email>",
  "first_name(optional)": "string ",
  "last_name(optional)": "string",
  "bio(optional)": "string ",
  "role(optional)": "string"
}
```

Получение пользователя по username:

**GET** ```/api/v1/users/{username}/```

Изменение данных пользователя по username:

**PATCH** ```/api/v1/users/{username}/```
```
{
  "username": "string",
  "email": "string <email>",
  "first_name(optional)": "string ",
  "last_name(optional)": "string",
  "bio(optional)": "string ",
  "role(optional)": "string"
}
```

Удаление пользователя по username:

**DELETE** ```/api/v1/users/{username}/```

Получение данных своей учетной записи:

**GET** ```/api/v1/users/me/```

Изменение данных своей учетной записи:

**PATCH** ```/api/v1/users/me/```
```
{
  "username": "string",
  "email": "string <email>",
  "first_name(optional)": "string ",
  "last_name(optional)": "string",
  "bio(optional)": "string "
}
```


## Авторы проекта - Александр Петров (sasa9089@yandex.ru), Кристина Стадникова(ururusenka32@yandex.ru),  Алексей Назарычев(Yois@mail.ru).
