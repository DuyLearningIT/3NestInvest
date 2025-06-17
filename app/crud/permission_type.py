from sqlalchemy.orm import Session, load_only, joinedload
from app.models import PermissionType
from app.schemas import PermissionTypeCreate, PermissionTypeUpdate
from datetime import datetime
from fastapi import HTTPException, status
from app.utils import get_internal_server_error, get_permission_type_or_404


async def create_permission_type(db: Session, request: PermissionTypeCreate):
	try:
		check = db.query(PermissionType).filter(PermissionType.permission_type_name == request.permission_type_name).first()
		if check:
			return {
				'mess' : 'Permission type has alread existed !',
				'status_code': status.HTTP_400_BAD_REQUEST
			}
		data = PermissionType(
			permission_type_name = request.permission_type_name,
			description = request.description
		)
		db.add(data)
		db.commit()
		db.refresh(data)
		return{
			'mess' : 'Create permission type successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data' : data
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_permission_types(db: Session):
	try:
		data = db.query(PermissionType).all()
		return {
			'mess' : 'Get permission types successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : data
		}
	except Exception as ex:
		return get_internal_server_error(ex)
	
async def update_permission_type(db: Session, request: PermissionTypeUpdate):
	try:
		check = get_permission_type_or_404(db, request.permission_type_id)
		check.permission_type_name = request.permission_type_name or check.permission_type_name
		check.description = request.description or check.description
		check.updated_at = datetime.utcnow()
		
		db.commit()
		db.refresh(check)
		return {
			'mess' : 'Update permission type successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : check
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def delete_permission_type(db: Session, request_id: int):
	try:
		check = get_permission_type_or_404(db, request_id)
		db.delete(check)
		db.commit()
		return {
			'mess' : 'Delete permission type successfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		return get_internal_server_error(ex)
	
async def get_permission_type(db: Session, request_id : int):
	try:
		check = get_permission_type_or_404(db, request_id)
		return {
			'mess' : 'Get permission type successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : check
		}
	except Exception as ex:
		return get_internal_server_error(ex)