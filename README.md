# Rout3 dashboard

Control plane for [Rout3](https://github.com/llm-proxy/llm-proxy): a small LLM proxy so an app can talk to one API while the backend picks among providers (OpenAI, Gemini, Mistral, and others via LiteLLM).

This repo is the **dashboard + API** (accounts, encrypted provider keys, routing config, playground chat). The proxy library itself lives in `llm-proxy/llm-proxy`.

**Status:** the team built this in summer 2024 (Rout3). Everyone else stopped around August 2024. I kept a few fixes into late 2025 and then left it. It is not an active product.

It is deployed at [rout3.com](https://rout3.com) / [rout3.vercel.app](https://rout3.vercel.app).

## What works

- Auth (JWT)
- Store provider API keys (Fernet-encrypted at rest)
- Issue a Rout3 API key for the proxy
- Configure models, timeout, temperature, max tokens
- Chat playground against the configured router
- FastAPI + Turso/SQLite, Svelte 4 + Vite frontend

## What does not

- **Billing / Stripe** — never integrated. The billing page is an explicit placeholder.
- **Analytics / revenue charts** — usage writes were commented out; the analytics page does not invent numbers.
- Tests — there is no test suite.

## Layout

```
dashboard/     Svelte UI
api-server/    FastAPI app
```

## Run locally

### API

```bash
cd api-server
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

`.env` needs `JWT_SIGNING_KEY`, `FERNET_KEY1`, `FERNET_KEY2`, and Turso `TURSO_DATABASE_URL` / `TURSO_AUTH_TOKEN` (or point `database.py` at local SQLite). Optional `SQL_ECHO=1` to log SQL.

On first boot `init_db()` creates a seed user `a` / `password` for local use. Change that before exposing the API.

### Dashboard

```bash
cd dashboard
npm install
cp .env.example .env
npm run dev
```

Set `VITE_API_URL` to the API, including `/api/v1` (default in the example is `http://localhost:8000/api/v1`).
