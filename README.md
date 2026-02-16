# Shortlist Discord Bot (Python)

Ein modular entwickelter Discord-Bot auf Basis von `discord.py`.  
Das Projekt demonstriert Kenntnisse in API-Integration, asynchroner Programmierung (async/await), Datenpersistenz (SQLite) sowie strukturierter Softwareorganisation.

## Funktionen

### Moderation
- Verwarnsystem mit Datenbankspeicherung (SQLite)
- Anzeigen aller Verwarnungen eines Nutzers
- Timeout (Mute) und Unmute Befehle
- Moderations-Logging in separatem Kanal

### Community Features
- Automatische Willkommensnachricht bei neuen Mitgliedern
- Level- und XP-System mit Cooldown gegen Spam
- Leaderboard der aktivsten Nutzer

### Slash-Commands
`/ping` – Bot Status prüfen  
`/warn` – Nutzer verwarnen  
`/warnings` – Verwarnungen anzeigen  
`/mute` – Nutzer temporär stummschalten  
`/unmute` – Stummschaltung aufheben  
`/rank` – Eigenes Level anzeigen  
`/leaderboard` – Rangliste anzeigen  
`/say` – Admin-Ankündigung

---

## Technologien
- Python 3.12
- discord.py (Discord API Wrapper)
- SQLite mit aiosqlite
- python-dotenv (Konfigurationsmanagement)
- Asynchrone Programmierung (async/await)

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

