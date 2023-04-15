# Проект API для Yatube
API сервис для социальной сети Yatube

### Технологии:
+ Python3  
+ Django
+ Django REST Framework 

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/sasa9089/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### После запуска проекта, доступна документация для API Yatube: 
### http://127.0.0.1:8000/redoc/
В документации описаны доступные адреса и команды.
Документация представлена в формате Redoc.


## Автор проекта - Александр Петров (sasa9089@yandex.ru)
