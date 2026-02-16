# Shortlist Discord Bot (Python)

Modularer Discord-Bot (discord.py) mit Moderation, Logging, Welcome-Automation und Level/XP-System.
Projekt erstellt als Portfolio für Bewerbungen (saubere Struktur, Async, SQLite-Persistenz, Slash-Commands).

## Features
- Slash Commands: `/ping`, `/say`, `/warn`, `/warnings`, `/mute`, `/unmute`, `/rank`, `/leaderboard`
- Moderation: Warnsystem (SQLite) + Timeouts
- Logging in einen separaten Channel
- Welcome Message bei Server-Join
- Level/XP System mit Cooldown gegen Spam

## Tech Stack
- Python 3.12
- discord.py
- SQLite (aiosqlite)
- python-dotenv

## Setup
1. `python -m venv .venv`  
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `.env` anlegen (siehe `.env.example`)
5. `python bot.py`

## Screenshots (optional, empfohlen)
- /ping
- Warnsystem
- /rank + leaderboard
- Welcome Message
# Shortlist Discord Bot (Python)

Ein modular aufgebauter Discord-Bot mit Moderationssystem, Logging, Welcome-Automation und Level-System.

## Funktionen
- Slash Commands (/ping, /rank, /leaderboard)
- Moderationssystem (Warnungen + Timeouts)
- Welcome-Nachricht bei neuen Mitgliedern
- Level- und XP-System mit Cooldown
- Persistente Speicherung mit SQLite

## Technologien
- Python 3
- discord.py
- SQLite (aiosqlite)
- Async Programming (async/await)

## Ziel
Das Projekt dient als Portfolio-Projekt, um Kenntnisse in API-Integration, Event-Handling, Datenpersistenz und Softwarestruktur zu demonstrieren.
