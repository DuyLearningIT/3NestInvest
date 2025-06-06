from fastapi import APIRouter, Depends
from app.schemas import CRUDType, UpdateType
from app.db import db_depend
from app.crud import type as type_crud
from app.utils import admin_required

router = APIRouter(
	prefix = '/types',
	tags=['Types']
)

# Admin required
@router.post('/create-type')
async def create_type(db: db_depend, request: CRUDType, admin= Depends(admin_required)):
	response = await type_crud.create_type(db, request)
	return response

@router.get('/get-types')
async def get_types(db: db_depend):
	response = await type_crud.get_types(db)
	return response

@router.get('/get-type')
async def get_type(db: db_depend, type_id: int):
	response = await type_crud.get_type(db, type_id)
	return response

# Admin required
@router.post('/update-type')
async def update_type(db: db_depend, request : UpdateType, admin= Depends(admin_required)):
	response = await type_crud.update_type(db, request, admin)
	return response

# Admin required
@router.delete('/delete-type')
async def delete_type(db: db_depend, type_id: int, admin= Depends(admin_required)):
	response = await type_crud.delete_type(db, type_id)
	return response