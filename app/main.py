from fastapi import FastAPI
from .database import Base, engine
from .auth.router import router as auth_router
from .metrics.router import router as metrics_router
from .metrics.collector import get_summary
from .database import SessionLocal
from .models import MetricHistory
from .alert import check_and_alert
from apscheduler.schedulers.background import BackgroundScheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Server Health Monitor API",
    description="Monitor CPU, RAM, Disk, dan Processes via REST API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(metrics_router)

def collect_metrics():
    db = SessionLocal()
    try:
        data = get_summary()
        cpu = data["cpu"]["cpu_percent"]
        ram = data["ram"]["ram_percent"]
        disk = data["disk"]["disk_percent"]
        
        record = MetricHistory(
            cpu_percent=cpu,
            ram_percent=ram,
            disk_percent=disk
        )
        db.add(record)
        db.commit()
        
        check_and_alert(cpu, ram, disk)
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(collect_metrics, "interval", minutes=5)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
def root():
    return {"message": "Server Health Monitor API is running"}