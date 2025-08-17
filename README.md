# Email Classifier API (⚡ FastAPI + 🦙 Ollama)

A lightweight, **CPU‑only** service that classifies incoming e‑mails (e.g. *spam*, *authentic*, *phishing*) using local **LLM models** served by Ollama. It is production‑ready yet hackable—swap models per request, retrain monthly, or scale out via Docker Compose.

---

## ✨ Key Features

| Capability                 | Details                                                                          |
| -------------------------- | -------------------------------------------------------------------------------- |
| **Multi‑model**            | Pass `?model=gemma3:1b`, `llama3:8b`, or any custom GGUF—you decide per request. |
| **CPU‑friendly**           | Works on a t2.micro or Raspberry Pi; set `OLLAMA_CPU_ONLY=true`.                 |
| **Lazy pulling & caching** | First request for a model triggers `ollama pull`; future calls are instant.      |
| **Clear folder structure** | Domain logic, API layer, and infra wrappers live in separate packages.           |
| **Dockerised**             | One‑command spin‑up via `docker‑compose up --build`.                             |
| **Observability‑ready**    | Add `prometheus-fastapi-instrumentator` in seconds for `/metrics`.               |

---

## 🗂️ Repository Layout

```
email-classifier/
├─ app/                # Python package
│  ├─ core/            # settings & logging
│  ├─ models/          # Pydantic schemas
│  ├─ services/        # model registry & business logic
│  ├─ api/v1/          # versioned REST endpoints
│  └─ main.py          # FastAPI factory
├─ tests/              # pytest suite
├─ Dockerfile          # app image
├─ docker-compose.yml  # app + Ollama
├─ requirements.txt    # pinned deps
└─ README.md           # you are here
```

---

## 🚀 Quick Start

### 1 · Clone & run locally (native Ollama)

```sh
# prerequisites: Python 3.12+, Ollama 0.6+
ollama serve &                      # start daemon in the background
ollama pull gemma3:1b llama3:8b     # or any models you like

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload       # http://localhost:8000/docs
```

\### 2 · Docker Compose

```sh
git clone https://github.com/abhishek0071/Email-Classifier-API.git
cd email-classifier

# first run may take a minute while models download
docker compose up --build
```

Visit **[http://localhost:8000/docs](http://localhost:8000/docs)** for an interactive Swagger UI.

---

## 🔌 Environment Variables

| Variable         | Default               | Purpose                            |
| ---------------- | --------------------- | ---------------------------------- |
| `OLLAMA_URL`     | `http://ollama:11434` | Base URL for the Ollama daemon     |
| `DEFAULT_MODEL`  | `gemma3:1b`           | Fallback model when none specified |
| `ALLOWED_MODELS` | `gemma3:1b,llama3:8b` | Comma‑separated allow‑list         |
| `MAX_TOKENS`     | `3000`                 | Clip generation length             |

Create a **.env** file or set them in `docker-compose.yml`.

---

## 📡 API Usage

### POST `/v1/classify`

Classify an e‑mail with optional model override.

```sh
curl -X POST 'localhost:8000/v1/classify?model=llama3:8b' \
     -H 'Content-Type: application/json' \
     -d '{"subject":"Win","body":"You have won a prize…"}'
# → {"label":"spam","model_used":"llama3:8b","latency_ms":87.4}
```

Check Swagger docs or `tests/test_classifier.py` for more examples.

---

## 🧩 Adding New Models

1. Convert your Hugging Face checkpoint to **GGUF** (quantised):

```sh
   python llama.cpp/convert.py <HF_MODEL> --outfile myspam.gguf --outtype q4_0
```

2. Register with Ollama:

```sh
   ollama create myspam --path myspam.gguf
```

3. Append to `ALLOWED_MODELS` and you’re done—no code change needed.

---

## 🛠️ Testing

```sh
pip install pytest
pytest -q
```

---

## 🏗️ Production Tips

* **Gunicorn workers** → `gunicorn -k uvicorn.workers.UvicornWorker app.main:app -w 4 -b 0.0.0.0:8000`
* **Observability** →

```python
  from prometheus_fastapi_instrumentator import Instrumentator
  Instrumentator().instrument(app).expose(app)
```

* **Rate‑limit** with `slowapi` or an API gateway.
* **Secure** Ollama & API ports behind a VPN or reverse proxy with mTLS.
* **Background retrain** via Celery + cron; on completion call `ollama create spam‑v2 …`.

---

## 🤝 Contributing

PRs and issues are welcome! Please format with `ruff`, run `pytest`, and update docs.

---

## 📄 License

MIT © 2025 Your Name / Webappclouds Software Solution Pvt Ltd