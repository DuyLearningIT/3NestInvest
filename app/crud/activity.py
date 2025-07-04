from sqlalchemy.orm import Session, load_only, joinedload
from app.models import ActivityLog, User
from datetime import datetime
from fastapi import Query, status
from app.utils import get_internal_server_error

# Filter all 
async def get_activity_logs_filtered(
    db: Session,
    user_email: str = None,
    entity: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    page: int = 1,
    limit: int = 50
):
    try:
        skip = (page - 1) * limit

        query = db.query(ActivityLog, User.user_email).join(User, ActivityLog.user_id == User.user_id)

        if user_email:
            query = query.filter(User.user_email == user_email.strip())

        if entity:
            query = query.filter(ActivityLog.target_type == entity.strip())

        if start_date and end_date:
            query = query.filter(ActivityLog.created_at.between(start_date, end_date))

        total = query.count()

        results = (
            query.order_by(ActivityLog.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        logs = []
        for log, email in results:
            logs.append({
                'log_activity_id': log.activity_log_id,
                'user_id': log.user_id,
                'user_email': email,
                'activity_description': log.activity_description,
                'target_type': log.target_type,
                'created_at': log.created_at.isoformat(),
                'ip' : log.ip
            })

        return {
            'mess': 'Filtered user activities',
            'status_code': status.HTTP_200_OK,
            'data': logs,
            'pagination': {
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': (total + limit - 1) // limit
            }
        }
    except Exception as ex:
        return get_internal_server_error(ex)
