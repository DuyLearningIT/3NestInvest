from sqlalchemy.orm import Session, load_only, joinedload
from app.models import PermissionType, Permission
from app.schemas import PermissionTypeCreate, PermissionTypeUpdate
from datetime import datetime
from fastapi import HTTPException, status
from app.utils import get_internal_server_error, get_permission_type_or_404, get_permission_or_404


async def create_permission(db: Session, request: PermissionCreate):
	try:
		check = db.query(Permission).filter(Permission.permission_name == request.permission_name).first()
		if check:
			return {
				'mess' : 'Permission has already existed !',
				'status_code' : status.HTTP_400_BAD_REQUEST
			}
		permission = Permission(
			permission_name = request.permission_name,
			description = request.description,
			permission_type_id = request.permission_type_id
		)
		db.add(permission) 
		db.commit()
		db.refresh(permission)
		return {
			'mess' : 'Add permission successfully !',
			'status_code': status.HTTP_201_CREATED, 
			'data' : permission
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_permissions(db: Session):
	try:
		return {
			'mess' : 'Get all permissions successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : db.query(Permission).all()
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_permission(db: Session, request_id):
	try:
		check = get_permission_or_404(db, request_id)
		return {
			'mess' : 'Get permission successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : check
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_permissions_by_type(db: Session, request_id):
	try:
		permissions = (
			db.query(Permission, PermissionType.permission_type_name)
			.join(PermissionType, Permission.permission_type_id = PermissionType.permission_type_id)
			.filter(Permission.permission_type_id == request_id)
			.all()
		)
		return {
			'mess' : 'Get permissions by permission type successfully !',
			'status_code' : status.HTTP_200_OK,
			'data'  : permissions
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def update_permission(db: Session, request: PermissionUpdate):
	try:
		check = get_permission_or_404(db, request.permission_id)
		check.permission_name = request.permission_name or check.permission_name
		check.description = request.descriptiom or check.description
		check.permission_type_id = request.permission_type_id or check.permission_type_id

		db.commit()
		db.refresh(check)
		return {
			'mess' : 'Update pemission successfully!',
			'status_code' : status.HTTP_200_OK,
			'data' : check
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def delete_permission(db: Session, request_id):
	try:
		check = get_permission_or_404(db, request_id)
		db.delete(check)
		db.commit()
		return {
			'mess' : 'Delete permission successfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		return get_internal_server_error(ex)
