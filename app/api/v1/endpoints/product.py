from fastapi import APIRouter, Depends, Request
from app.schemas import CreateProduct, UpdateProduct
from app.db import db_depend
from app.crud import product as product_crud
from app.utils import admin_required, get_current_user

router = APIRouter(
	prefix = '/products',
	tags=['Products']
)

@router.get('/get-products')
async def get_products(db: db_depend, logRequest: Request, current_user = Depends(get_current_user)):
	response = await product_crud.get_products(db, logRequest, current_user)
	return response

@router.get('/get-product')
async def get_products(db: db_depend, product_id : int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await product_crud.get_product(db, product_id, logRequest, current_user)
	return response

@router.get('/get-products-by-category')
async def get_products_by_category(db: db_depend, category_id : int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await product_crud.get_products_by_category(db, category_id, logRequest, current_user)
	return response

@router.get('/get-products-by-type')
async def get_products_by_type(db: db_depend, type_id : int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await product_crud.get_products_by_type(db, type_id, logRequest, current_user)
	return response

# Admin required
@router.post('/create-product')
async def create_product(db: db_depend, request: CreateProduct, logRequest: Request, current_user = Depends(get_current_user)):
	response = await product_crud.create_product(db, request, logRequest, current_user)
	return response

# Admin required
@router.post('/update-product')
async def update_product(db: db_depend, request: UpdateProduct, logRequest: Request, current_user = Depends(get_current_user)):
	response = await product_crud.update_product(db, request, logRequest, current_user)
	return response

# Admin required
@router.delete('/delete-product')
async def delete_product(db: db_depend, product_id : int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await product_crud.delete_product(db, product_id, logRequest, current_user)
	return response

# User required
@router.get('/get-products-by-role')
async def get_products_by_role(db: db_depend, logRequest: Request, current_user = Depends(get_current_user)):
	response = await product_crud.get_products_by_role(db, logRequest, current_user)
	return response

# Admin required
@router.get('/get-products-by-role-and-type')
async def get_products_by_role_and_type(db: db_depend, role_id: int, type_id : int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await product_crud.get_products_by_role_and_type(db, role_id, type_id, logRequest, current_user)
	return response

# User required
@router.get('/get-products-by-category-and-role')
async def get_products_by_category_and_role(db : db_depend, category_id: int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await product_crud.get_products_by_category_and_role(db, category_id, logRequest, current_user)
	return response