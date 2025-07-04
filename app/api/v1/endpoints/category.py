from fastapi import APIRouter, Depends, Request
from app.schemas import CreateCategory, UpdateCategory
from app.db import db_depend
from app.crud import category as category_crud
from app.utils import admin_required, get_current_user

router = APIRouter(
	prefix = '/categories',
	tags=['Categories']
) 

@router.post('/create-category')
async def create_category(db: db_depend, request: CreateCategory, logRequest: Request, current_user= Depends(get_current_user)):
	response = await category_crud.create_category(db, request, logRequest, current_user)
	return response

@router.get('/get-categories')
async def get_categories(db : db_depend, logRequest: Request, current_user= Depends(get_current_user)):
	response = await category_crud.get_categories(db, logRequest, current_user)
	return response

@router.get('/get-category')
async def get_category(db: db_depend, category_id : int, logRequest: Request, current_user= Depends(get_current_user)):
	response = await category_crud.get_category(db, category_id, logRequest, current_user)
	return response

@router.post('/update-category')
async def update_category(db : db_depend, request: UpdateCategory, logRequest: Request, current_user= Depends(get_current_user)):
	response = await category_crud.update_category(db, request, logRequest, current_user)
	return response

@router.delete('/delete-category')
async def delete_category(db: db_depend, category_id : int, logRequest: Request, current_user= Depends(get_current_user)):
	response = await category_crud.delete_category(db, category_id, logRequest, current_user)
	return response

@router.get('/get-categories-by-type')
async def get_categories_by_type(db: db_depend, type_id : int, logRequest: Request, current_user= Depends(get_current_user)):
	response = await category_crud.get_categories_by_type(db, type_id, logRequest, current_user)
	return response