from fastapi import APIRouter, Depends, Request
from app.schemas import OrderCreate, OrderUpdate, OrderApprove
from app.db import db_depend
from app.crud import order as order_crud
from app.utils import get_current_user, admin_required, high_level_required

router = APIRouter(
	prefix = '/orders',
	tags=['Orders']
)

# User required
@router.post('/create-order')
async def create_order(db: db_depend, request : OrderCreate, logRequest: Request, current_user= Depends(get_current_user)):
	response = await order_crud.create_order(db, request, logRequest, current_user)
	return response

# High-level required
@router.get('/get-orders')
async def get_orders(db: db_depend, logRequest: Request, current_user= Depends(get_current_user)):
	response = await order_crud.get_orders(db, logRequest, current_user)
	return response

# User required
@router.get('/get-orders-by-user')
async def get_orders_by_user(db: db_depend, logRequest: Request, current_user = Depends(get_current_user)):
	response = await order_crud.get_orders_by_user(db, logRequest, current_user)
	return response

# User required
@router.post('/update-order')
async def update_order(db: db_depend, request : OrderUpdate, logRequest: Request, current_user = Depends(get_current_user)):
	response = await order_crud.update_order(db, request, logRequest, current_user)
	return response

# User required
@router.get('/get-order')
async def get_order(db: db_depend, order_id: int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await order_crud.get_order(db, order_id, logRequest, current_user)
	return response

# High-level required
@router.post('/change-status-of-order')
async def change_status_of_order(db: db_depend, request: OrderApprove, logRequest: Request, high_level = Depends(high_level_required)):
	response = await order_crud.change_status_of_order(db, request, logRequest, high_level)
	return response

# User required
@router.get('/get-order-details-by-order')
async def get_order_details_by_order(db: db_depend, order_id: int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await order_crud.get_order_details_by_order(db, order_id, logRequest, current_user)
	return response

# User required
@router.delete('/delete-order')
async def delete_order(db: db_depend, order_id: int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await order_crud.delete_order(db, order_id, logRequest, current_user)
	return response

# High level required
@router.get('/get-orders-by-role')
async def get_orders_by_role(db: db_depend, role_id: int, logRequest: Request, high_level= Depends(high_level_required)):
	response = await order_crud.get_orders_by_role(db, role_id, logRequest, high_level)
	return response

# User required
@router.get('/get-orders-by-user')
async def get_orders_by_user(db: db_depend, logRequest: Request, current_user = Depends(get_current_user)):
	response = await order_crud.get_orders_by_user(db, logRequest, current_user)
	return response

# User required 
@router.get('/get-orders-by-deal')
async def get_orders_by_deal(db: db_depend, deal_id: int, logRequest: Request, current_user= Depends(get_current_user)):
	response = await order_crud.get_orders_by_deal(db, deal_id, logRequest, current_user)
	return response