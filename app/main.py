from fastapi import FastAPI
from .database import Base, engine
from .auth.router import router as auth_router
from .metrics.router import router as metrics_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Server Health Monitor API",
    description="Monitor CPU, RAM, Disk, dan Processes via REST API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(metrics_router)

@app.get("/")
def root():
    return {"message": "Server Health Monitor API is running"}