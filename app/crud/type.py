from sqlalchemy.orm import Session, load_only
from app.models import Type
from app.schemas import CRUDType, UpdateType
from datetime import datetime
from fastapi import HTTPException, status

# Admin required
async def create_type(db: Session, request : CRUDType):
	try:
		check = db.query(Type).filter(Type.type_name == request.type_name).first()
		if check:
			raise HTTPException(
				detail= 'Type has already existed !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		new_type = Type(
			type_name = request.type_name,
			description = request.description
		)
		db.add(new_type)
		db.commit()
		db.refresh(new_type)

		return {
			'mess' : 'Create type successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data' : {
				'type_id' : new_type.type_id,
				'type_name' : new_type.type_name,
				'description' : new_type.description,
				'created_at' : new_type.created_at,
				'created_by' : new_type.created_by
			}
		}	
	except Exception as ex:
		raise HTTPException(
			detail= f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

async def get_types(db: Session):
	try:
		return {
			'mess': 'Get all types successfully !',
			'status_code' : status.HTTP_200_OK,
			'data': db.query(Type).options(load_only(Type.type_id, Type.type_name, Type.description)).all()
		}
	except Exception as ex:
		raise HTTPException(
			detail= f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

async def get_type(db : Session, type_id : int):
	try:
		check = db.query(Type).filter(Type.type_id == type_id).first()
		if check is None:
			raise HTTPException(
				detail= 'Type not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		return {
			'mess' : 'Get type successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : {
				'type_id' : check.type_id,
				'type_name' : check.type_name,
				'description' : check.description
			}
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# Admin required
async def update_type(db: Session, request: UpdateType, admin : dict):
	try:
		check = db.query(Type).filter(Type.type_id == request.type_id).first()
		if check is None:
			raise HTTPException(
				detail= 'Type not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		check.type_name = request.type_name or check.type_name
		check.description = request.description or check.description
		check.updated_at = datetime.now()
		check.updated_by = admin['user_name']

		db.commit()
		db.refresh(check)
		return {
			'mess' : 'Update type successfully !',
			'status_code': status.HTTP_200_OK,
			'data': {
				'type_id' : check.type_id,
				'type_name' : check.type_name,
				'description' : check.description,
				'updated_at': check.updated_at,
				'updated_by' : check.updated_by
			}
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# Admin required
async def delete_type(db: Session, type_id : int):
	try:
		check = db.query(Type).filter(Type.type_id == type_id).first()
		if check is None:
			raise HTTPException(
				detail= 'Type not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		db.delete(check)
		db.commit()
		return {
			'mess' : 'Delete type successfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)