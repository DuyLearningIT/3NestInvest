from fastapi import APIRouter, Depends
from app.schemas import DealCreate, DealUpdate
from app.db import db_depend
from app.crud import deal as deal_crud
from app.utils import admin_required, high_level_required, get_current_user

router = APIRouter(
	prefix = '/deals',
	tags=['Deals']
)

# High-level required
@router.get('/get-deals')
async def get_deals(db: db_depend, high_level = Depends(high_level_required)):
	response = await deal_crud.get_deals(db)
	return response

# User required
@router.get('/get-deal')
async def get_deal(db: db_depend, deal_id : int , current_user = Depends(get_current_user)):
	response = await deal_crud.get_deal(db, deal_id)
	return response

# User required
@router.post('/create-deal')
async def create_deal(db: db_depend, request: DealCreate, current_user = Depends(get_current_user)):
	respnse = await deal_crud.create_deal(db, request, current_user)
	return response

# User required
@router.post('/update-deal')
async def update_deal(db: db_depend, request: DealUpdate, current_user= Depends(get_current_user)):
	response = await deal_crud.update_deal(db, request, current_user)
	return response

# User required
@router.delete('/delete-deal')
async def delete_deal(db: db_depend, deal_id: int, current_user= Depends(get_current_user)):
	response = deal_crud.delete_deal(db, deal_id, current_user)
	return response

# High-level required
@router.post('/change-status-of-deal')
async def change_status_of_deal(db: db_depend, deal_id: int, status: str, high_level = Depends(high_level_required)):
	response = deal_crud.change_status_of_deal(db, deal_id, str)
	return response