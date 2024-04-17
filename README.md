# Фудграм - продуктовый помощник

Приложение для создания рецептов.

# Установка
## Локально

1. Клонировать репозиторий
2. Заполнить файл **.env** в соответствии с **env.example**
2. Собрать и запутить контейнеры:
    ```
    docker compose up
    ```
3. Выполнить миграции (обязательно), заполнить список ингредиентов, создать суперпользователя (опционально):
    ```
    docker container exec foodgram_backend python3 manage.py migrate
    docker container exec foodgram_backend python3 manage.py import
    docker container exec foodgram_backend python3 manage.py createsuperuser
    ```

4. Собрать статику бэкэнда и скопировать её для раздачи нгинксом:
    ```
    docker container exec foodgram_backend python3 manage.py collectstatic
    docker container exec foodgram_backend cp -r /app/collected_static/. /backend_static/static/
    ```

## В продакшен

0. Заполнить файл **.env** в соответствии с **env.example**; заполнить необходимые для действия **deploy** секреты в репозитории.
1. Использовать github action **deploy**;
2. Заполнить список ингредиентов, создать суперпользователя (опционально):
    ```
    docker compose -f docker-compose.production.yml exec backend python3 manage.py import
    docker compose -f docker-compose.production.yml exec backend manage.py createsuperuser
    ```

Или:
1. Скопировать файл docker-compose.production.yml на сервер
2. Заполнить файл **.env** в соответствии с **env.example**
3. Запустить контейнеры, собрать статику бэкенда, скопировать ее для раздачи нгинксом:
    ```
    docker compose -f docker-compose.production.yml pull
    docker compose -f docker-compose.production.yml down
    docker compose -f docker-compose.production.yml up -d
    docker compose -f docker-compose.production.yml exec backend python3 manage.py migrate
    docker compose -f docker-compose.production.yml exec backend python3 manage.py collectstatic
    docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
    ```
4. Заполнить список ингредиентов, создать суперпользователя (опционально):
    ```
    docker compose -f docker-compose.production.yml exec backend python3 manage.py import
    docker compose -f docker-compose.production.yml exec backend manage.py createsuperuser
    ```

# Документация api
Документация доступна при запущенных контейнерах на эндпойнте `/api/docs/`
