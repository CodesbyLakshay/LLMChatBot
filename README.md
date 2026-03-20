# LLM ChatBot

An AI-powered document chatbot built with FastAPI. Upload a PDF, TXT, or DOCX file and ask questions about it — the bot answers strictly from the document's content using Groq's LLM API.

**Live Demo:** https://llmchatbot-ksqn.onrender.com
**GitHub:** https://github.com/CodesbyLakshay/LLMChatBot

---

## What it does

1. Register and log in with a secure account
2. Upload a document (PDF, TXT, DOCX)
3. Ask any question about the document
4. Get answers strictly from the document — no hallucination, no outside knowledge

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (async) |
| Database | SQLite + SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Auth | JWT (PyJWT) + Argon2 password hashing |
| LLM | Groq API — `meta/llama-4-scout-17b-16e-instruct` |
| PDF Parsing | PyMuPDF (fitz) |
| DOCX Parsing | python-docx |
| Deployment | Render |

---

## Project Structure

```
LLMChatBot/
├── app/
│   ├── core/
│   │   └── utils.py           # JWT + password hashing
│   ├── models/
│   │   ├── user.py            # users table
│   │   └── document.py        # documents table
│   ├── routers/
│   │   ├── auth.py            # /auth/register /auth/login /auth/me
│   │   └── chat.py            # /chat/upload /chat/ask /chat/documents
│   ├── schemas/
│   │   ├── user.py            # Pydantic request/response shapes
│   │   └── chat.py
│   ├── services/
│   │   ├── text_extractor.py  # PDF/DOCX/TXT parsing
│   │   └── ai_groq.py         # Groq API integration
│   ├── config.py              # Environment settings
│   ├── database.py            # Async SQLAlchemy engine + session
│   └── main.py                # FastAPI app entry point
├── alembic/                   # Database migrations
├── static/
│   └── index.html             # Frontend UI
├── requirements.txt
├── render.yaml
└── .env.example
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Create account |
| POST | `/auth/login` | No | Login, get JWT token |
| GET | `/auth/me` | Yes | Get current user profile |
| POST | `/chat/upload` | Yes | Upload a document |
| POST | `/chat/ask` | Yes | Ask a question about a document |
| GET | `/chat/documents` | Yes | List all uploaded documents |

Full interactive docs at `/docs` (Swagger UI).

---

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/CodesbyLakshay/LLMChatBot.git
cd LLMChatBot

# 2. Create virtual environment with Python 3.11
python3.11 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and fill in GROQ_API_KEY and SECRET_KEY

# 5. Run database migrations
alembic upgrade head

# 6. Start the server
uvicorn app.main:app --reload
```

App runs at: http://localhost:8000
Swagger UI at: http://localhost:8000/docs

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Get free at https://console.groq.com |
| `SECRET_KEY` | Random secret for JWT signing — run `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |
| `DATABASE_URL` | `sqlite:///./llm_chatbot.db` |
| `UPLOAD_DIR` | `uploads` |

---

## References

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [SQLAlchemy Async Docs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Docs](https://alembic.sqlalchemy.org)
- [Groq API Docs](https://console.groq.com/docs)
- [PyJWT Docs](https://pyjwt.readthedocs.io)
- [PyMuPDF Docs](https://pymupdf.readthedocs.io)

---

## Notes

- The backend API (routes, models, auth, DB, AI integration) was written by me
- The frontend UI (`static/index.html`) was generated with AI assistance
- SQLite is used for simplicity — can be swapped to PostgreSQL by changing `DATABASE_URL`
