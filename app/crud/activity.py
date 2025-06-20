from sqlalchemy.orm import Session, load_only, joinedload
from app.models import ActivityLog
from datetime import datetime
from fastapi import Query, status
from app.utils import get_internal_server_error

async def get_activity_logs(db: Session, page: int = 1, limit: int = 50):
	try:
		skip = (page - 1) * limit
		total = db.query(ActivityLog).count()
		logs = db.query(ActivityLog).offset(skip).limit(limit).all()

		return {
			'mess': 'Get user activities',
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


async def get_activity_logs_by_entity(db: Session, entity: str, page: int = 1, limit: int = 50):
	try:
		skip = (page - 1) * limit
		total = db.query(ActivityLog).count()
		logs = db.query(ActivityLog).filter(ActivityLog.target_type == entity.strip()).offset(skip).limit(limit).all()

		return {
			'mess': 'Get user activities',
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
	
async def get_activity_logs_by_user(db: Session, user_id: int, page: int = 1, limit: int = 50):
	try:
		skip = (page - 1) * limit
		total = db.query(ActivityLog).count()
		logs = db.query(ActivityLog).filter(ActivityLog.user_id == user_id).offset(skip).limit(limit).all()

		return {
			'mess': 'Get user activities',
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
