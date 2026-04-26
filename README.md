[README.md](https://github.com/user-attachments/files/27107482/README.md)
# 🤖 UserBot

A lightweight **Telegram bot** built with Python and [aiogram 3](https://docs.aiogram.dev/), backed by a PostgreSQL database and fully containerized with Docker.

---

## ✨ Features

- **aiogram 3** — modern async Telegram bot framework
- **PostgreSQL** — persistent data storage via `psycopg2`
- **Docker Compose** — one-command deployment with isolated services
- **Environment-based config** — secrets managed through `.env` files
- **HTML parse mode** — rich message formatting out of the box
- **Auto-restart** — bot and database containers restart automatically on failure

---

## 🗂️ Project Structure

```
UserBot/
├── app/
│   └── bot/
│       ├── bot_main.py      # Dispatcher & router setup
│       └── dispatcher.py    # Token & middleware config
├── database/                # DB models and queries
├── main.py                  # Entry point
├── Dockerfile
├── docker-compose.yml
├── req.txt                  # Python dependencies
├── copy_env                 # Env setup helper
└── db_query                 # Raw DB query utilities
```

---

## ⚙️ Configuration

Copy the example env file and fill in your values:

```bash
cp copy_env .env
```

| Variable      | Description              |
|---------------|--------------------------|
| `DB_USER`     | PostgreSQL username       |
| `DB_PASSWORD` | PostgreSQL password       |
| `DB_HOST`     | Database host             |
| `DB_PORT`     | Database port (default `5432`) |
| `DB_NAME`     | Database name             |

> Add your Telegram bot token inside `app/bot/dispatcher.py` as `TOKEN`.

---

## 🛠️ Tech Stack

| Layer      | Technology                     |
|------------|-------------------------------|
| Language   | Python 3                      |
| Bot Framework | aiogram 3.27               |
| Database   | PostgreSQL + psycopg2         |
| HTTP Client | aiohttp 3                    |
| Containers | Docker & Docker Compose       |
| Config     | python-dotenv                 |

---
