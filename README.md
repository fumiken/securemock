# 🔐 securemock

A secure, ephemeral mock API server with a Python CLI and FastAPI backend.

**securemock** lets you register mock API endpoints from the command line, with expiration, one-time use, and header-matching support.

---

## 🚀 Features

- ✅ Register mock APIs via CLI
- ⏱ Expire mock endpoints after a given time
- 🔁 One-time-use endpoints with `--once`
- 🎯 Match specific headers with `--match-headers`
- 💾 Persistent storage with `mock_data.json`
- 🔥 FastAPI backend, built for simplicity and speed

---

## 📦 Installation

```bash
git clone https://github.com/your-username/securemock.git
cd securemock
pip install -e .
```

---

## 🧪 Usage

### 1. Start the server

```bash
securemock runserver
```

### 2. Create a basic mock

```bash
securemock create \
  --path /hello \
  --method GET \
  --status 200 \
  --response '{"message": "Hello"}' \
  --expire 60
```

### 3. Access the mock

```bash
curl http://localhost:8000/hello
```

---

## 🧨 One-time mock

```bash
securemock create \
  --path /once \
  --method GET \
  --status 200 \
  --response '{"message": "This will self-destruct"}' \
  --once
```

---

## 🎯 Match headers

```bash
securemock create \
  --path /auth-only \
  --method GET \
  --status 200 \
  --response '{"message": "Welcome"}' \
  --match-headers '{"X-API-KEY": "secret123"}'
```

```bash
curl -H "X-API-KEY: secret123" http://localhost:8000/auth-only
```

---

## 💾 Persistence

Mocks are saved to `mock_data.json`. They persist across restarts unless expired or deleted.

---

## 🧰 Development

```bash
python -m securemock.cli runserver
```

To reinstall after changes:

```bash
pip install -e .
```

---

## 📄 License

This software is provided under a **custom proprietary license**.  
You may **not** modify, redistribute, or use this software for commercial purposes without explicit permission.  
See the [LICENSE](./LICENSE) file for details.
