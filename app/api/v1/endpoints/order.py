from fastapi import APIRouter, Depends
from app.schemas import OrderCreate, OrderUpdate
from app.db import db_depend
from app.crud import order as order_crud
from app.utils import get_current_user

router = APIRouter(
	prefix = '/orders',
	tags=['Orders']
)

@router.post('/create-order')
async def create_order(db: db_depend, request : OrderCreate, current_user= Depends(get_current_user)):
	response = order_crud.create_order(db, request, current_user)
	return response

@router.get('/get-orders')
async def get_orders(db: db_depend):
	response = order_crud.get_orders(db)
	return response

@router.get('/get-order-by-user')
async def get_order_by_user(db: db_depend, current_user = Depends(get_current_user)):
	response = order_crud.get_order_by_user(db, current_user)
	return response

@router.post('/update-order')
async def update_order(db: db_depend, request : OrderUpdate ,current_user = Depends(get_current_user)):
	response = order_crud.update_order(db, current_user)
	return response