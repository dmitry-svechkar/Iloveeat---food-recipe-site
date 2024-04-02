### I LOVE EAT 
##### Сайт для размещения информации о рецептах разных кухон мира. 

![image](https://github.com/dmitry-svechkar/foodgram-project-react/assets/138603861/fec36985-98c7-46b1-b508-c44ea5098411)


В проекте реализованы:
- Аутентификация и регистрация пользователей.
- Полностью настроен REST API для:
   - Добавления рецептов
   - Функционал добавления подписок на авторов
   - Функционал добавления рецептов в избранное
   - Выгрузка списка покупок для готовки.
- Подключен front на базе react-приложения
- Импорт данных в БД.
- Настроена админка для управления ресурсами сайта.

### Стек технологий
<div>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/django/django-plain.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/djangorest/djangorest-line-wordmark.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nginx/nginx-original.svg" width="50" height="50">
          
</div>

##### Чтобы запустить проект на локальной машине:
###### Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:dmitry-svechkar/foodgram-project-react.git
```
###### Создать в корневой папке файл .env и заполнить данными своего проекта и БД.
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
###### Перейти в папку infra и оттуда выполнить команду
```
cd infra
```
```
docker compose up -d
```
###### Выполнить команды по миграции и сбору статики из контейнера backend
```
python3 manage.py migrate
python3 manage.py collectstatic
```
###### Один раз скопировать статику при разворачивании проекта:
```
cp -r /app/static/. /backend_static/
```
###### Из контейнера backend выполните команду по созданию суперпользователя
```
python manage.py createsuperuser
```
###### В проекте заготовлена тестовая база. Чтобы ее загрузить в БД выполните команду:

```
python manage.py import_data
```

###### API документация доступна по адресу:
```
127.0.0.1:8000/api/
```

######  Приготовить вкусный ужин вечером!

