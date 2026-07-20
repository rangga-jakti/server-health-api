# 🖥️ Server Health Monitor API

A REST API built with FastAPI to monitor Linux/Windows server health in real-time — CPU, RAM, Disk, and Processes.

## 🚀 Tech Stack

- **FastAPI** — Modern Python web framework
- **PostgreSQL** — Database for metric history
- **SQLAlchemy** — ORM
- **JWT Auth** — Secure endpoint access
- **psutil** — System metrics collector

## 📡 Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register user | ❌ |
| POST | `/auth/login` | Login & get JWT token | ❌ |
| GET | `/metrics/cpu` | CPU usage & frequency | ✅ |
| GET | `/metrics/ram` | RAM usage | ✅ |
| GET | `/metrics/disk` | Disk usage | ✅ |
| GET | `/metrics/processes` | Top 10 processes by CPU | ✅ |
| GET | `/metrics/summary` | All metrics at once + save to DB | ✅ |
| GET | `/metrics/history` | Last 20 metric records | ✅ |

## ⚙️ Setup

```bash
# Clone repo
git clone https://github.com/rangga-jakti/server-health-api.git
cd server-health-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your database credentials

# Run
uvicorn app.main:app --reload
```

## 🔐 Authentication

Register and login to get a JWT token, then use it in the Authorization header:

## 📊 Example Response `/metrics/summary`

```json
{
  "cpu": {
    "cpu_percent": 37.3,
    "cpu_count": 4,
    "cpu_freq": { "current": 2500, "min": 0, "max": 2501 }
  },
  "ram": {
    "total": 17066700800,
    "available": 6581542912,
    "used": 10485157888,
    "ram_percent": 61.4
  },
  "disk": {
    "total": 127911088128,
    "used": 126841823232,
    "free": 1069264896,
    "disk_percent": 99.2
  }
}
```

## 📁 Project Structure

server-health-api/
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── auth/
│ │ ├── router.py
│ │ └── utils.py
│ └── metrics/
│ ├── router.py
│ └── collector.py
├── .env
├── requirements.txt
└── README.md