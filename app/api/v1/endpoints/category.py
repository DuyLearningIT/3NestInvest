from fastapi import APIRouter, Depends
from app.schemas import CreateCategory, UpdateCategory
from app.db import db_depend
from app.crud import category as category_crud
from app.utils import admin_required

router = APIRouter(
	prefix = '/categories',
	tags=['Categories']
) 

# Admin required
@router.post('/create-category')
async def create_category(db: db_depend, request: CreateCategory, admin= Depends(admin_required)):
	response = category_crud.create_category(db, request, admin)
	return response

@router.get('/get-categories')
async def get_categories(db : db_depend):
	response = category_crud.get_categories(db)
	return response

@router.get('/get-category')
async def get_category(db: db_depend, category_id : int):
	response = category_crud.get_category(db, category_id)
	return response

# Admin required
@router.post('/update-category')
async def update_category(db : db_depend, request: UpdateCategory, admin= Depends(admin_required)):
	response = category_crud.update_category(db, request, admin)
	return response

# Admin required
@router.delete('/delete-category')
async def delete_category(db: db_depend, category_id : int, admin= Depends(admin_required)):
	response = category_crud.delete_category(db, category_id, admin)
	return response

@router.get('/get-categories-by-type')
async def get_categories_by_type(db: db_depend, type_id : int):
	response = category_crud.get_categories_by_type(db, type_id)
	return response	