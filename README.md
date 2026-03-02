# KanMind Backend API

KanMind ist ein Django REST Framework Backend für eine Task- und Kanban-Anwendung.

Das Projekt stellt eine REST API mit Token-basierter Authentifizierung bereit
und dient als Backend für ein externes Frontend.

Dieses Projekt wurde im Rahmen der Developer Akademie umgesetzt.

---

## 🚀 Features

- Token Authentication (DRF)
- Board-System mit Owner + Members
- Task CRUD API
- Comment-System
- Benutzer-Zuweisung (Assignee / Reviewer)
- Board-basierte Zugriffskontrolle
- Filter: assigned-to-me / reviewing
- SQLite Datenbank
- CORS-Unterstützung
- Automatisierte Tests mit pytest

---

## 🧱 Tech Stack

- Python 3
- Django 6.0.1
- Django REST Framework 3.16.1
- SQLite
- pytest

---

## ⚙️ Installation & Setup

### 1. Repository klonen

```bash
git clone <REPOSITORY_URL>
cd kanmind_backend


2. Virtuelle Umgebung erstellen
python -m venv venv
3. Aktivieren

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
4. Dependencies installieren
pip install -r requirements.txt
5. Migrationen ausführen
python manage.py migrate
6. Server starten
python manage.py runserver

Backend läuft unter:

http://127.0.0.1:8000/
🔐 Authentifizierung
Login
POST /api/login/

Request Body:

{
  "username": "username",
  "password": "password"
}

Response:

{
  "token": "abc123..."
}

Token im Header mitsenden:

Authorization: Token <DEIN_TOKEN>
📌 Boards API
Methode	Endpoint	Beschreibung
GET	/api/boards/	Eigene Boards
POST	/api/boards/	Neues Board erstellen
GET	/api/boards/<id>/	Board Details
PATCH	/api/boards/<id>/	Board bearbeiten
DELETE	/api/boards/<id>/	Board löschen

Board Owner gilt automatisch als Member.

📋 Tasks API
Methode	Endpoint	Beschreibung
GET	/api/tasks/	Tasks aus eigenen Boards
POST	/api/tasks/	Task erstellen
GET	/api/tasks/<id>/	Task Details
PATCH	/api/tasks/<id>/	Task bearbeiten
DELETE	/api/tasks/<id>/	Nur Creator oder Board Owner
GET	/api/tasks/assigned-to-me/	Mir zugewiesene Tasks
GET	/api/tasks/reviewing/	Tasks zur Überprüfung
Permissions

Nur Board Members sehen Tasks

Nur Creator oder Board Owner dürfen löschen

Board kann nach Erstellung nicht geändert werden

💬 Comments API
Methode	Endpoint	Beschreibung
GET	/api/tasks/<id>/comments/	Kommentare anzeigen
POST	/api/tasks/<id>/comments/	Kommentar erstellen
DELETE	/api/tasks/<task_id>/comments/<comment_id>/	Nur Author
🧪 Tests

Alle Tests werden mit pytest ausgeführt.

pytest -q

Aktueller Status:

6 passed
📌 Projektstruktur
kanmind_backend/
├── authentication/
├── boards/
├── tasks/
├── core/
├── manage.py
├── requirements.txt
└── README.md
👤 Autor

Muhammed Yunus Amini
Developer Akademie