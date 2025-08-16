# NewsPortal – Django Capstone

A news application where Readers view approved articles, Editors review/approve, and Journalists publish. Includes DRF API filtered by Reader subscriptions. Final database: MariaDB (port 3307).

## Tech
- Django 5
- Django REST Framework
- Custom User model (roles: Reader, Editor, Journalist)
- Groups/permissions auto-managed via signals
- MariaDB (PyMySQL) on Windows

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver