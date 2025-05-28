from fastapi import APIRouter, Depends
from app.schemas import OrderCreate, OrderUpdate
from app.db import db_depend
from app.crud import order as order_crud
from app.utils import get_current_user, admin_required

router = APIRouter(
	prefix = '/orders',
	tags=['Orders']
)

# User required
@router.post('/create-order')
async def create_order(db: db_depend, request : OrderCreate, current_user= Depends(get_current_user)):
	response = order_crud.create_order(db, request, current_user)
	return response

# Admin required
@router.get('/get-orders')
async def get_orders(db: db_depend, admin= Depends(admin_required)):
	response = order_crud.get_orders(db)
	return response

# User required
@router.get('/get-order-by-user')
async def get_order_by_user(db: db_depend, current_user = Depends(get_current_user)):
	response = order_crud.get_order_by_user(db, current_user)
	return response

# User required
@router.post('/update-order')
async def update_order(db: db_depend, request : OrderUpdate ,current_user = Depends(get_current_user)):
	response = order_crud.update_order(db, current_user)
	return response

# User required
@router.get('/get-order')
async def get_order(db: db_depend, order_id: int, current_user = Depends(get_current_user)):
	response = order_crud.get_order(db, order_id)
	return response

# Admin required
@router.post('/change-status-of-order')
async def change_status_of_order(db: db_depend, status: str, order_id : int, admin = Depends(admin_required),):
	response = order_crud.change_status_of_order(db, admin, status, order_id)
	return response