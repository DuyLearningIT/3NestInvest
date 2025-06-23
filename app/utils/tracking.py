import requests
from fastapi import Request
from sqlalchemy.orm import Session
from app.models import ActivityLog  

def get_location(ip: str) -> str:
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        data = res.json()
        return f"{data.get('city', '')}, {data.get('regionName', '')}, {data.get('country', '')}"
    except Exception:
        return "Unknown"

def log_activity(
    db: Session,
    request: Request,
    user_id: int,
    activity_description: str,
    target_type: str
) -> None:
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host

    agent = request.headers.get("user-agent", "Unknown")
    location = get_location(ip)

    log = ActivityLog(
        user_id=user_id,
        activity_description=activity_description,
        target_type=target_type,
        ip=ip,
        agent=agent,
        location=location
    )

    db.add(log)
    db.commit()
