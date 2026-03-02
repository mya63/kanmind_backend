# KanMind Backend API

KanMind is a Django REST Framework backend for a task and kanban application.

It provides a REST API with token-based authentication and is designed to be used by an external frontend.

This project was built as part of the Developer Akademie.

---

## 🚀 Features

- Token Authentication (DRF)
- Board system with Owner and Members
- Task CRUD API
- Comment system
- User assignment (Assignee / Reviewer)
- Board-based access control
- Filters: assigned-to-me / reviewing
- SQLite database
- CORS support
- Automated tests with pytest (96% coverage in tasks app)

---

## 🧱 Tech Stack

- Python 3
- Django 6.0.1
- Django REST Framework 3.16.1
- SQLite
- pytest

---

## ⚙️ Installation & Setup

### 1. Clone repository

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
5. Run migrations
python manage.py migrate
6. Start server
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

Send the token in the header:

Authorization: Token <YOUR_TOKEN>
📌 Boards API
Method	Endpoint	Description
GET	/api/boards/	List user boards
POST	/api/boards/	Create board
GET	/api/boards/<id>/	Board details
PATCH	/api/boards/<id>/	Update board
DELETE	/api/boards/<id>/	Delete board

Board owner is automatically considered a member.

📋 Tasks API
Method	Endpoint	Description
GET	/api/tasks/	List tasks from user boards
POST	/api/tasks/	Create task
GET	/api/tasks/<id>/	Task details
PATCH	/api/tasks/<id>/	Update task
DELETE	/api/tasks/<id>/	Only creator or board owner
GET	/api/tasks/assigned-to-me/	Tasks assigned to current user
GET	/api/tasks/reviewing/	Tasks where user is reviewer
Task Permissions

Only board members can see tasks

Only the creator or the board owner can delete a task

The board of a task cannot be changed after creation

💬 Comments API
Method	Endpoint	Description
GET	/api/tasks/<id>/comments/	List comments
POST	/api/tasks/<id>/comments/	Create comment
DELETE	/api/tasks/<task_id>/comments/<comment_id>/	Only the author
🧪 Tests

Run tests:

pytest -q
pytest --cache-clear

Current status:

31 tests

96% coverage in tasks app

All tests passing

📁 Project Structure
kanmind_backend/
├── authentication/
├── boards/
├── tasks/
├── core/
├── manage.py
├── requirements.txt
└── README.md
👤 Author

Muhammed Yunus Amini
Developer Akademie