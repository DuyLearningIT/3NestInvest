from fastapi import APIRouter 
from app.schemas import CreateCategory, UpdateCategory
from app.db import db_depend
from app.crud import category as category_crud

router = APIRouter(
	prefix = '/categories',
	tags=['Categories']
) 
@router.post('/create-category')
async def create_category(db: db_depend, request: CreateCategory):
	response = category_crud.create_category(db, request)
	return response

@router.get('/get-categories')
async def get_categories(db : db_depend):
	response = category_crud.get_categories(db)
	return response

@router.get('/get-category')
async def get_category(db: db_depend, category_id : int):
	response = category_crud.get_category(db, category_id)
	return response

@router.post('/update-category')
async def update_category(db : db_depend, request: UpdateCategory):
	response = category_crud.update_category(db, request)
	return response

@router.delete('/delete-category')
async def delete_category(db: db_depend, category_id : int):
	response = category_crud.delete_category(db, category_id)
	return response