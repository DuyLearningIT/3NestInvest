from fastapi import APIRouter 
from app.schemas import CreateProduct, UpdateProduct
from app.db import db_depend
from app.crud import product as product_crud

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

@router.post('/create-product')
async def create_product(db: db_depend, request: CreateProduct):
	response = product_crud.create_product(db, request)
	return response

@router.post('/update-product')
async def update_product(db: db_depend, request: UpdateProduct):
	response = product_crud.update_product(db, request)
	return response

@router.delete('/delete-product')
async def delete_product(db: db_depend, product_id : int):
	response = product_crud.delete_product(db, product_id)
	return response