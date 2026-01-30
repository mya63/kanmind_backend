# KanMind Backend API

Dieses Projekt ist ein **Django REST Framework Backend** für eine einfache Notiz-Anwendung.
Es stellt eine **REST API mit Token-basierter Authentifizierung** bereit.

Das Projekt wurde im Rahmen der **Developer Akademie** umgesetzt.

---

## 🚀 Features

- Django REST Framework
- Token Authentication (Login per API)
- Geschützte Endpunkte
- CRUD-API für Notizen
- SQLite Datenbank
- CORS-Unterstützung
- API-Tests mit Postman

---

## 🧱 Tech Stack

- Python 3
- Django 6.0.1
- Django REST Framework
- SQLite
- Postman

---

## 📁 Projektstruktur

kanmind_backend/
├── kanmind/ # Projekt-Settings & Root-URLs
├── core/ # API App (Views, URLs)
├── db.sqlite3 # Datenbank
├── .env # Environment Variablen (nicht im Repo)
├── .gitignore
└── README.md


---

## 🔐 Environment Variablen

Der Django `SECRET_KEY` wird über eine `.env` Datei geladen.

### `.env`
```env
DJANGO_SECRET_KEY=django-insecure-xxxxxxxxxxxxxxxx

▶️ Projekt starten

python manage.py runserver


🔑 Authentifizierung (Token Login)

/api/login/

Request Body (JSON):

{
  "username": "dein_username",
  "password": "dein_passwort"
}

Response:

{
  "token": "abc123..."
}

📝 Notes API

GET /api/notes/

Header Authorization: Token <DEIN_TOKEN>


Neue Notiz erstellen

POST /api/notes/

Body (JSON): 

{
  "title": "Neue Notiz",
  "content": "Inhalt aus Postman"
}

Einzelne Notiz abrufen

GET /api/notes/<id>/

🧪 API Tests

Alle Endpunkte wurden erfolgreich mit Postman getestet:

Login (Token erhalten)

Authentifizierte Requests

GET / POST Notizen

📌 Hinweis

Dieses Projekt ist ein reines Backend (API-only).
Ein Frontend ist nicht Teil dieser Abgabe, kann aber problemlos angebunden werden.

👤 Autor

Muhammed Yunus Amini
Developer Akademie