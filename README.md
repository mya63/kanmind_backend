KanMind Backend API

KanMind is a Django REST Framework backend for a task and kanban application.

It provides a REST API with token-based authentication and is designed to work with an external frontend.

This project was built as part of the Developer Akademie.


🚀 Features

Token authentication

Boards with owner and members

Task CRUD API

Comment system

Task assignment (assignee / reviewer)

Board-based access control

SQLite database

Automated tests with pytest


🧱 Tech Stack

Python

Django

Django REST Framework

SQLite

pytest


⚙️ Installation
Clone repository
git clone <REPOSITORY_URL>
cd kanmind_backend
Create virtual environment
python -m venv venv
Activate environment

Windows

venv\Scripts\activate

Mac / Linux

source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Run migrations

python manage.py migrate

Start server

python manage.py runserver

Backend runs on:

http://127.0.0.1:8000/

🔐 Authentication

Login endpoint:

POST /api/login/

Example request:

{
  "username": "username",
  "password": "password"
}

Example response:

{
  "token": "abc123..."
}

Use the token in request headers:

Authorization: Token <YOUR_TOKEN>

🧪 Tests

Run tests:

pytest


👤 Author

Muhammed Yunus Amini
Developer Akademie