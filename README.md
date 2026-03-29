Frontend (Live App):
https://mya63.github.io/project.KanMind/
# KanMind Backend API

KanMind is a **Django REST Framework backend** for a task and kanban application.

It provides a **REST API with token-based authentication** and is designed to work with an external frontend.

This project was built as part of the **Developer Akademie**.

---

# 🚀 Features

* Token authentication
* Boards with **owner and members**
* Task CRUD API
* Comment system
* Task assignment (**assignee / reviewer**)
* Board-based access control
* SQLite database
* Automated tests with **pytest**

---

# 🧱 Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* pytest

---

# ⚙️ Installation

## Clone repository

```bash
git clone <REPOSITORY_URL>
cd kanmind_backend
```

## Create virtual environment

```bash
python -m venv venv
```

## Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Mac / Linux

```bash
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run migrations

```bash
python manage.py migrate
```

## Start server

```bash
python manage.py runserver
```

Backend runs on:

```
http://127.0.0.1:8000/
```

---

# 🔐 Authentication

## Login endpoint

```
POST /api/login/
```

### Example request

```json
{
  "username": "username",
  "password": "password"
}
```

### Example response

```json
{
  "token": "abc123..."
}
```

Use the token in request headers:

```
Authorization: Token <YOUR_TOKEN>
```

---

# 🧪 Tests

Run tests with:

```bash
pytest
```

---

# 👤 Author

Muhammed Yunus Amini


