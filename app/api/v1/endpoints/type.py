from fastapi import APIRouter, Depends, Request
from app.schemas import CRUDType, UpdateType
from app.db import db_depend
from app.crud import type as type_crud
from app.utils import get_current_user

router = APIRouter(
	prefix = '/types',
	tags=['Types']
)

@router.post('/create-type')
async def create_type(db: db_depend, request: CRUDType, logRequest: Request, current_user = Depends(get_current_user)):
	response = await type_crud.create_type(db, request, logRequest, current_user)
	return response

@router.get('/get-types')
async def get_types(db: db_depend, logRequest: Request, current_user = Depends(get_current_user)):
	response = await type_crud.get_types(db, logRequest, current_user)
	return response

@router.get('/get-type')
async def get_type(db: db_depend, type_id: int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await type_crud.get_type(db, type_id, logRequest, current_user)
	return response


@router.post('/update-type')
async def update_type(db: db_depend, request : UpdateType, logRequest: Request, current_user = Depends(get_current_user)):
	response = await type_crud.update_type(db, request, logRequest, current_user)
	return response


@router.delete('/delete-type')
async def delete_type(db: db_depend, type_id: int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await type_crud.delete_type(db, type_id, logRequest, current_user)
	return response