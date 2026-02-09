# KanMind Backend API

Dieses Projekt ist ein **Django REST Framework Backend** für eine einfache
**Task- und Kanban-Anwendung (KanMind)**.

Es stellt eine **REST API mit token-basierter Authentifizierung** bereit
und dient als Backend für ein externes Frontend.

Das Projekt wurde im Rahmen der **Developer Akademie** umgesetzt.

---

## 🚀 Features

- Django REST Framework
- Token-basierte Authentifizierung
- Geschützte API-Endpunkte
- CRUD-API für Tasks
- Benutzerzuweisung (Assigned / Reviewer)
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

# KanMind Backend API

Dieses Projekt ist ein **Django REST Framework Backend** für eine einfache
**Task- und Kanban-Anwendung (KanMind)**.

Es stellt eine **REST API mit token-basierter Authentifizierung** bereit
und dient als Backend für ein externes Frontend.

Das Projekt wurde im Rahmen der **Developer Akademie** umgesetzt.

---

## 🚀 Features

- Django REST Framework
- Token-basierte Authentifizierung
- Geschützte API-Endpunkte
- CRUD-API für Tasks
- Benutzerzuweisung (Assigned / Reviewer)
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
├── core/ # API App (Models, Views, Serializer, URLs)
├── db.sqlite3 # SQLite Datenbank
├── .env # Environment Variablen (nicht im Repository)
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

Backend läuft anschließend unter:
http://127.0.0.1:8000/


🔑 Authentifizierung (Token Login)

Login Endpoint:

POST /api/login/



Request Body (JSON):

{
  "username": "dein_username",
  "password": "dein_passwort"
}



Response:

{
  "token": "abc123..."
}



Der Token muss bei allen geschützten Requests
im Header mitgesendet werden:

Authorization: Token <DEIN_TOKEN>



📋 Tasks API
Alle Tasks abrufen:

GET /api/tasks/

Task erstellen:

POST /api/tasks/

json:
{
  "title": "Neue Aufgabe",
  "description": "Beschreibung",
  "status": "todo"
}


Einzelnen Task abrufen / ändern / löschen:

GET    /api/tasks/<id>/
PATCH  /api/tasks/<id>/
DELETE /api/tasks/<id>/

Aufgaben des eingeloggten Users:

GET /api/tasks/assigned-to-me/


Aufgaben zur Überprüfung:

GET /api/tasks/reviewing/


🧪 API Tests

Alle Endpunkte wurden erfolgreich mit Postman getestet:

Login (Token erhalten)

Authentifizierte Requests

CRUD-Operationen für Tasks

Benutzerbezogene Filter (assigned / reviewing)


📌 Hinweis

Dieses Projekt ist ein reines Backend (API-only).
Ein Frontend kann über HTTP/Fetch problemlos angebunden werden.


👤 Autor

Muhammed Yunus Amini
Developer Akademie