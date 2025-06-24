from sqlalchemy.orm import Session
from app.models import ChangeManagement
from app.schemas import ChangeCreate, ChangeUpdate
from datetime import datetime
from fastapi import HTTPException, status
from app.utils import get_internal_server_error, get_permission_type_or_404, get_permission_or_404


async def create_change_management(db: Session, request: ChangeUpdate):
	try:
		new_change = ChangeManagement(
			change_description = request.change_description,
			requested_by = request.requested_by
		)
		db.add(new_change)
		db.commit()
		db.refresh(new_change)
		return{
			'mess' : 'Create change successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data' : new_change
		}
	except Exception as ex:
		return get_internal_server_error(ex)


async def update_change(db: Session, request: ChangeUpdate):
	try:
		check = db.query(ChangeManagement).filter(ChangeManagement.change_id == request.change_id).first()
		if not check:
			return {
				'mess' : 'Change not found !',
				'status_code' : status.HTTP_404_NOT_FOUND,
			}
		
		check.requested_by = request.requested_by or check.requested_by
		check.change_description = request.change_description or check.change_description
		db.commit()
		db.refresh(check)
		return {
			'mess' : 'Update change successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : check
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_changes(db: Session):
	try:
		return {
			'mess' : 'Get all changes successfully !',
			'status_code': status.HTTP_200_OK,
			'data': db.query(ChangeManagement).all()
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_change(db: Session, request_id: int):
	try:
		check = db.query(ChangeManagement).filter(ChangeManagement.change_id == request_id).first()
		if not check:
			return {
				'mess' : 'Change not found !',
				'status_code' : status.HTTP_404_NOT_FOUND,
			}
		return {
			'mess': 'Get change successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : check
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def delete_change(db: Session, request_id : int):
	try:
		check = db.query(ChangeManagement).filter(ChangeManagement.change_id == request_id).first()
		if not check:
			return {
				'mess' : 'Change not found !',
				'status_code' : status.HTTP_404_NOT_FOUND,
			}
		db.delete(check)
		db.commit()
		return {
			'mess' : 'Delete change successfully !',
			'status_code': status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		return get_internal_server_error(ex)