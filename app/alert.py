import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Failed to send alert: {e}")

def check_and_alert(cpu: float, ram: float, disk: float):
    alerts = []
    
    if cpu > 80: 
        alerts.append(f"⚠️ <b>CPU tinggi!</b> Usage: {cpu}%")
    if ram > 85:
        alerts.append(f"⚠️ <b>RAM tinggi!</b> Usage: {ram}%")
    if disk > 90:
        alerts.append(f"🚨 <b>Disk hampir penuh!</b> Usage: {disk}%")
    
    if alerts:
        message = "🖥️ <b>Server Health Alert</b>\n\n" + "\n".join(alerts)
        send_telegram_alert(message)