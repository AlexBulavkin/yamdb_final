### Краткое описание проекта YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Произведения разделяются по категриям и жанрам.

### Шаблон наполнения env-файла
```
SECRET_KEY=p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
### Запуск контейнера и приложения

Перейти в репозиторий для запуска docker:

```
cd infra/
```

Запуск docker-compose:

```
docker-compose up -d --build
```

Проведите миграции:

```
docker-compose exec web python manage.py migrate
```

Cоздайте суперпользователя

```
docker-compose exec web python manage.py createsuperuser
```

Остановку контейнеров проведите командой

```
docker-compose down -v 
```

### Автор проекта

alexbulavkin

### Стек технологий
gunicorn, Nginx, Docker, docker-compose, PostgreSQL

### Workflow
![result of workflow](https://github.com/alexbulavkin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)