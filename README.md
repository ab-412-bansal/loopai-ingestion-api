# Loop.ai Data Ingestion API

A Flask-based asynchronous data ingestion system built for the Loop.ai assessment.  
This API supports priority-based ingestion requests with batch processing, rate limiting, and status tracking.

---

## 🚀 Features

- 📩 Submit data ingestion requests with priority (`HIGH`, `MEDIUM`, `LOW`)
- 🔄 Processes IDs in batches of 3
- 🕔 Enforces global rate limit (1 batch per 5 seconds)
- 🔧 Prioritizes HIGH over LOW, with FIFO for same priority
- 📊 Real-time status tracking via `/status/<ingestion_id>`
- ✅ Asynchronous batch processing using threads
- 🧪 Fully tested with `pytest`

---

## 📁 Project Structure

```
loopai_ingestion_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py         # Flask app with /ingest and /status
│   ├── tasks.py        # Queue logic and processing engine
│   └── models.py       # Data schemas
│
├── tests/
│   └── test_api.py     # Automated tests using pytest
│
├── requirements.txt    # All required dependencies
└── README.md
```

---

## ⚙️ Requirements

- Python 3.7+
- Flask
- pytest

---

## 💻 Local Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/loopai-ingestion-api.git
cd loopai-ingestion-api
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask App
```bash
python -m app.main
```

### 5. Access the API
- `POST` → [http://localhost:5000/ingest](http://localhost:5000/ingest)
- `GET`  → [http://localhost:5000/status/<ingestion_id>](http://localhost:5000/status/<ingestion_id>)

---

## 🧪 Running Tests

Make sure your environment is activated and `pytest` is installed:

```bash
# Set PYTHONPATH (PowerShell)
$env:PYTHONPATH="."
pytest
```

All tests are in `tests/test_api.py`.

---

## 📬 API Endpoints

### 🔹 `POST /ingest`

#### Request:
```json
{
  "ids": [1, 2, 3, 4, 5],
  "priority": "HIGH"
}
```

#### Response:
```json
{
  "ingestion_id": "abc123"
}
```

---

### 🔹 `GET /status/<ingestion_id>`

#### Response:
```json
{
  "ingestion_id": "abc123",
  "status": "triggered",
  "batches": [
    {"batch_id": "b1", "ids": [1, 2, 3], "status": "completed"},
    {"batch_id": "b2", "ids": [4, 5], "status": "triggered"}
  ]
}
```

---

## 🌐 Deployment (Railway)

1. Push this repo to GitHub
2. Go to [https://railway.app](https://railway.app)
3. Connect GitHub repo → Deploy
4. Set `Start Command` to:
   ```bash
   python -m app.main
   ```
5. Generate domain in **Settings > Domains**

---

## ✅ Submission Checklist

- [x] Public GitHub Repo with source code
- [x] Hosted Railway URL
- [x] Working `/ingest` and `/status/<ingestion_id>` endpoints
- [x] Complete README
- [x] `requirements.txt` with all dependencies
- [x] `tests/test_api.py` with passing tests

---

## 📎 Example Hosted URL

> `https://loopai-ingestion.up.railway.app`

---

## 👨‍💻 Author

Ayush Bansal — Loop.ai Assessment  
Roll Number - 2210993778<br>
Email - ayush3778.be22@chitkara.edu.in