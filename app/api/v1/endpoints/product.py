from fastapi import APIRouter, Depends
from app.schemas import CreateProduct, UpdateProduct
from app.db import db_depend
from app.crud import product as product_crud
from app.utils import admin_required, get_current_user

router = APIRouter(
	prefix = '/products',
	tags=['Products']
)

@router.get('/get-products')
async def get_products(db: db_depend):
	response = product_crud.get_products(db)
	return response

@router.get('/get-product')
async def get_products(db: db_depend, product_id : int):
	response = product_crud.get_product(db, product_id)
	return response

@router.get('/get-products-by-category')
async def get_products_by_category(db: db_depend, category_id : int):
	response = product_crud.get_products_by_category(db, category_id)
	return response

@router.get('/get-products-by-type')
async def get_products_by_type(db: db_depend, type_id : int):
	response = product_crud.get_products_by_type(db, type_id)
	return response

# Admin required
@router.post('/create-product')
async def create_product(db: db_depend, request: CreateProduct, admin=Depends(admin_required)):
	response = product_crud.create_product(db, request, admin)
	return response

# Admin required
@router.post('/update-product')
async def update_product(db: db_depend, request: UpdateProduct, admin=Depends(admin_required)):
	response = product_crud.update_product(db, request, admin)
	return response

# Admin required
@router.delete('/delete-product')
async def delete_product(db: db_depend, product_id : int, admin = Depends(admin_required)):
	response = product_crud.delete_product(db, product_id)
	return response

# User required
@router.get('/get-products-by-role')
async def get_products_by_role(db: db_depend, current_user = Depends(get_current_user)):
	response = product_crud.get_products_by_role(db, current_user)
	return response

# Admin required
@router.get('/get-products-by-role-and-type')
async def get_products_by_role_and_type(db: db_depend, role: str, type_id : int, admin = Depends(admin_required)):
	response = product_crud.get_products_by_role_and_type(db, role, type_id)
	return response

# User required
@router.get('/get-products-by-category-and-role')
async def get_products_by_category_and_role(db : db_depend, category_id: int, current_user = Depends(get_current_user)):
	response = product_crud.get_products_by_category_and_role(db, category_id, current_user)
	return response