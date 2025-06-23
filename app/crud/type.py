from sqlalchemy.orm import Session, load_only
from app.models import Type
from app.schemas import CRUDType, UpdateType
from datetime import datetime
from fastapi import HTTPException, status, Request
from app.utils import get_internal_server_error, get_type_or_404, log_activity
from app.utils.permission_checking import check_permission

async def create_type(db: Session, request : CRUDType, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'type', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		check = db.query(Type).filter(Type.type_name == request.type_name).first()
		if check:
			raise HTTPException(
				detail= 'Type has already existed !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		new_type = Type(
			type_name = request.type_name,
			type_description = request.type_description
		)
		db.add(new_type)
		db.commit()
		db.refresh(new_type)
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Create type",
			target_type= "Type"
		)
		return {
			'mess' : 'Create type successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data' : {
				'type_id' : new_type.type_id,
				'type_name' : new_type.type_name,
				'description' : new_type.type_description,
				'created_at' : new_type.created_at,
				'created_by' : new_type.created_by
			}
		}	
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_types(db: Session, logRequest: Request, current_user: dict):
	try:
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Get all types",
			target_type= "Type"
		)
		return {
			'mess': 'Get all types successfully !',
			'status_code' : status.HTTP_200_OK,
			'data': db.query(Type).options(load_only(Type.type_id, Type.type_name, Type.type_description)).all()
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_type(db : Session, type_id : int, logRequest: Request, current_user: dict):
	try:
		check = get_type_or_404(db, type_id)
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Get type by id",
			target_type= "Type"
		)
		return {
			'mess' : 'Get type successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : {
				'type_id' : check.type_id,
				'type_name' : check.type_name,
				'description' : check.type_description
			}
		}
	except Exception as ex:
		return get_internal_server_error(ex)


async def update_type(db: Session, request: UpdateType, logRequest: Request, current_user : dict):
	try:
		permission = await check_permission(db, 'manage', 'type', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		check = get_type_or_404(db, request.type_id)
		check.type_name = request.type_name or check.type_name
		check.type_description = request.type_description or check.type_description
		check.updated_at = datetime.now()
		check.updated_by = current_user['user_name']

		db.commit()
		db.refresh(check)
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Update type",
			target_type= "Type"
		)
		return {
			'mess' : 'Update type successfully !',
			'status_code': status.HTTP_200_OK,
			'data': {
				'type_id' : check.type_id,
				'type_name' : check.type_name,
				'description' : check.type_description,
				'updated_at': check.updated_at,
				'updated_by' : check.updated_by
			}
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def delete_type(db: Session, type_id : int, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'type', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		check = get_type_or_404(db, type_id)
		db.delete(check)
		db.commit()
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Delete type",
			target_type= "Type"
		)
		return {
			'mess' : 'Delete type successfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		return get_internal_server_error(ex)