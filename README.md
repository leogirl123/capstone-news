## Run locally (venv)
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Docker (MariaDB via Compose)
docker compose -p capstone up -d db
docker compose -p capstone run --rm web python manage.py migrate
docker compose -p capstone up web
# open http://localhost:8000

## Environment (.env)
DJANGO_SETTINGS_MODULE=newsportal.settings
SECRET_KEY=replace_me
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DB_BACKEND=mysql
MYSQL_DATABASE=newsdb
MYSQL_USER=newsuser
MYSQL_PASSWORD=newspass
MYSQL_HOST=db
MYSQL_PORT=3306

## Docs (Sphinx)
sphinx-apidoc -o docs newsportal
sphinx-build -b html docs docs\_build\html
