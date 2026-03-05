# KanMind Backend API

KanMind is a **Django REST Framework backend** for a task and kanban application.

It provides a REST API with **token-based authentication** and is designed to be used with an external frontend.

This project was built as part of the **Developer Akademie**.

---

# 🚀 Features

- Token Authentication (Django REST Framework)
- Board system with **Owner and Members**
- Task CRUD API
- Comment system
- User assignment (**Assignee / Reviewer**)
- Board-based access control
- Filters:
  - `assigned-to-me`
  - `reviewing`
- SQLite database
- CORS support for external frontend
- Automated tests with **pytest**

---

# 🧱 Tech Stack

- Python 3
- Django 6.0.1
- Django REST Framework 3.16.1
- SQLite
- pytest

---

# ⚙️ Installation & Setup

## 1. Clone repository

```bash
git clone <REPOSITORY_URL>
cd kanmind_backend

2. Create virtual environment
python -m venv venv
3. Activate environment
Windows
venv\Scripts\activate
Mac / Linux
source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Environment variables

Create a .env file based on .env.example.

Example:

SECRET_KEY=change-me
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
SQLITE_NAME=db.sqlite3
6. Run migrations
python manage.py migrate
7. Start server
python manage.py runserver

Backend runs on:

http://127.0.0.1:8000/
🔐 Authentication
Login
POST /api/login/

Request body:

{
  "username": "username",
  "password": "password"
}

Response:

{
  "token": "abc123..."
}

Send the token in the request header:

Authorization: Token <YOUR_TOKEN>
📌 Boards API
Method	Endpoint	Description
GET	/api/boards/	List user boards
POST	/api/boards/	Create board
GET	/api/boards/<id>/	Board details
PATCH	/api/boards/<id>/	Update board
DELETE	/api/boards/<id>/	Delete board

The board owner is automatically a member.

📋 Tasks API
Method	Endpoint	Description
GET	/api/tasks/	List tasks
POST	/api/tasks/	Create task
GET	/api/tasks/<id>/	Task details
PATCH	/api/tasks/<id>/	Update task
DELETE	/api/tasks/<id>/	Delete task

Additional filters:

Endpoint	Description
/api/tasks/assigned-to-me/	Tasks assigned to the current user
/api/tasks/reviewing/	Tasks where the user is reviewer

Task rules:

Only board members can see tasks

Only the creator or board owner can delete a task

The board of a task cannot be changed after creation

💬 Comments API
Method	Endpoint	Description
GET	/api/tasks/<id>/comments/	List comments
POST	/api/tasks/<id>/comments/	Create comment
DELETE	/api/tasks/<task_id>/comments/<comment_id>/	Delete comment (author only)
🧪 Tests

Run tests with:

pytest -q

Optional:

pytest --cache-clear

Current status:

31 tests

All tests passing

~96% coverage in the tasks app

📁 Project Structure
kanmind_backend/
│
├── authentication/
├── boards/
├── tasks/
│
├── manage.py
├── requirements.txt
└── README.md
👤 Author

Muhammed Yunus Amini

Developer Akademie