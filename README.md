# Foodgram

Foodgram - Продуктовый помощник. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Инструкция по запуску

### Локальный запуск

1. Склонируйте репозиторий на локальную машину:
   ```sh
   git clone https://github.com/K0ryaga/foodgram-project-react.git
   ```
2. Перейдите в директорию с проектом:
   ```sh
   cd foodgram-project-react
   ```
3. Создайте и активируйте виртуальное окружение:
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```
4. Перейдите в директорию `infra`:
   ```sh
   cd infra
   ```
5. Запустите `docker-compose.yml`:
   ```sh
   docker compose up -d
   ```
6. Выполните следующие команды в контейнере backend:
   ```sh
   docker exec -it infra-backend-1 python manage.py migrate
   docker exec -it infra-backend-1 python manage.py collectstatic
   docker exec -it infra-backend-1 python manage.py createsuperuser
   docker exec -it infra-backend-1 python manage.py load_ing
   ```

Готово! Проект доступен по адресам: `http://127.0.0.1:8000` и `http://localhost:8000`.

### Запуск на сервере

1. Подключитесь к своему серверу:
   ```sh
   ssh <server_user>@<server_IP>
   ```
2. Установите Docker:
   ```sh
   sudo apt install docker.io
   ```
3. Установите Docker Compose:
   ```sh
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```
4. Создайте и перейдите в директорию с проектом:
   ```sh
   mkdir foodgram && cd foodgram
   mkdir infra && cd infra
   touch .env
   ```
5. Заполните файл `.env` следующей информацией:
   ```env
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=foodgram
   POSTGRES_USER=foodgram_user
   POSTGRES_PASSWORD=foodgram_password
   DB_HOST=db
   DB_PORT=5432
   SECRET_KEY=<Your_some_long_string>
   DEBUG=False
   ALLOWED_HOSTS=<Your_host>
   ```
6. Скопируйте содержимое директории `infra` с локальной машины на сервер и запустите `docker-compose.yml`:
   ```sh
   sudo docker compose up -d
   ```
7. Узнайте ID или имя backend контейнера:
   ```sh
   sudo docker ps
   ```
8. Выполните следующие команды в контейнере backend:
   ```sh
   sudo docker exec -it <backend_container_id> python manage.py migrate
   sudo docker exec -it <backend_container_id> python manage.py collectstatic
   sudo docker exec -it <backend_container_id> python manage.py createsuperuser
   sudo docker exec -it <backend_container_id> python manage.py load_ing
   ```

Готово! Проект доступен по вашему домену и IP сервера на порту 8000.

## Использованные технологии

- Python
- Django
- Django REST framework
- Nginx
- Docker
- Postgres

## Автор проекта

Студент Яндекс.Практикума Антон Стыврин

[GitHub](https://github.com/K0ryaga)
