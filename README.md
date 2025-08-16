# News Application (Django Capstone)
## Local (venv)
py -m venv .venv
S:\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
## Docs
sphinx-build -b html docs docs\_build\html
## Docker
docker build -t news-app:latest .
docker run --rm --env-file .env news-app:latest python manage.py migrate
docker run --rm -p 8000:8000 --env-file .env news-app:latest
