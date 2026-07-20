from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import MetricHistory
from ..auth.utils import decode_token
from . import collector
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/metrics", tags=["metrics"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

@router.get("/cpu")
def cpu(user=Depends(get_current_user)):
    return collector.get_cpu()

@router.get("/ram")
def ram(user=Depends(get_current_user)):
    return collector.get_ram()

@router.get("/disk")
def disk(user=Depends(get_current_user)):
    return collector.get_disk()

@router.get("/processes")
def processes(user=Depends(get_current_user)):
    return collector.get_processes()

@router.get("/network")
def network(user=Depends(get_current_user)):
    return collector.get_network()

@router.get("/summary")
def summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    data = collector.get_summary()
    record = MetricHistory(
        cpu_percent=data["cpu"]["cpu_percent"],
        ram_percent=data["ram"]["ram_percent"],
        disk_percent=data["disk"]["disk_percent"]
    )
    db.add(record)
    db.commit()
    return data

@router.get("/history")
def history(db: Session = Depends(get_db), user=Depends(get_current_user)):
    records = db.query(MetricHistory).order_by(MetricHistory.recorded_at.desc()).limit(20).all()
    return records