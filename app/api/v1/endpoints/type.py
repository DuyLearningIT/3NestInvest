from fastapi import APIRouter 
from app.schemas import CRUDType, UpdateType
from app.db import db_depend
from app.crud import type as type_crud

router = APIRouter(
	prefix = '/types',
	tags=['Types']
)

@router.post('/create-type')
async def create_type(db: db_depend, request: CRUDType):
	try:
		data = type_crud.create_type(db, request)
		if data == False:
			return {
				'mess' : 'Type has already existsed !',
				'status_code' : 400
			}
		else:
			return {
				'mess' : 'Create type successfully !',
				'status_code' : 201
			}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong {ex}',
			'status_code' : 500
		}

@router.get('/get-types')
async def get_types(db: db_depend):
	try:
		data = type_crud.get_types(db)
		return {
			'mess' : 'Get all types successfully !',
			'data' : data,
			'status_code' : 200
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong {ex}',
			'status_code' : 500
		}

@router.get('/get-type')
async def get_type(db: db_depend, type_id: int):
	try:
		data = type_crud.get_type(db, type_id)
		if data is None:
			return {
				'mess' : 'Type not found !',
				'status_code' : 404
			}
		return {
			'mess' : 'Get type successfully !',
			'status_code' : 200,
			'data': data
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong {ex}',
			'status_code' : 500
		}

@router.post('/update-type')
async def update_type(db: db_depend, request : UpdateType):
	try:
		data = type_crud.update_type(db, request)
		if data is None:
			return {
				'mess' : 'Type not found !',
				'status_code' : 404
			}
		return {
			'mess' : 'Update type successfully !',
			'status_code' : 200,
			'data': data
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong {ex}',
			'status_code' : 500
		}

@router.delete('/delete-type')
async def delete_type(db: db_depend, type_id: int):
	try:
		check = type_crud.delete_type(db, type_id)
		if check == False:
			return{
				'mess' : 'Type not found !',
				'status_code' : 404
			}
		return{
			'mess' : 'Delete type successfully !',
			'status_code' : 204
		} 
	except Exception as ex:
		return {
			'mess' : f'Something was wrong {ex}',
			'status_code' : 500
		}