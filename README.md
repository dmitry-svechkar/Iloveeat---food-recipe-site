# Сайт для размещения информации о рецептах разных кухон мира.
Доступен по адресу https://recipesite-foodgram.zapto.org/recipes
Доступ для админки:
```
https://recipesite-foodgram.zapto.org/admin
```
```
login reviewer Пароль: Qwerty0527!
```
![image](https://github.com/dmitry-svechkar/foodgram-project-react/assets/138603861/fec36985-98c7-46b1-b508-c44ea5098411)

### Стек технологий

- Python 3.9
- Django 4.2.10
- DRF 3.14.0
- Postgres
- Docker
- Nginx

В проекте реализованы:
- Аутентификация и регистрация пользователей.
- Полностью настроенREST API для:
   - Добавления рецептов
   - Функционал добавления подписок на авторов
   - Функционал добавления рецептов в избранное
   - Выгрузка списка покупок для готовкию
- Импорт данных в БД.
- Настроена админка для управления ресурсами сайта.

# Чтобы запустить проект на локальной машине:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:dmitry-svechkar/foodgram-project-react.git
```
Создать в корневой папке файл .env и заполнить данными своего проекта и БД.
```
POSTGRES_USER=username
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=db_name
DB_HOST=db
DB_PORT=5432
SECRET_KEY=any_secret_key_of_django_project
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000
```
Перейти в папку infra и оттуда выполнить команду
```
cd infra
```
```
docker compose up -d
```
Один раз скопировать статику при разворачивании проекта:
```
cp -r /app/static/. /backend_static/
```
Из контейнера backend выполните команду по созданию суперпользователя
```
python manage.py createsuperuser
```
В проекте заготовлена тестовая база. Чтобы ее загрузить в БД выполните команду:
```
python manage.py import_data
```
