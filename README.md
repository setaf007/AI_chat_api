# AI Chat API

FastAPI backend with LM Studio (local LLM). User auth, chat history, rate limiting.

## Features
- JWT auth (register/login)
- Persistent chats per user
- Local AI via LM Studio
- Rate limiting
- SQLite + Alembic
- Auto API docs

1. **Clone & setup**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. **LM setup**
Currently tested using local LLM through LMstudio.
In order to use other API, code can be edited.
