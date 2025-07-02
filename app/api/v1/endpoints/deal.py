from fastapi import APIRouter, Depends, Request
from app.schemas import DealCreate, DealUpdate, DealApprove
from app.db import db_depend
from app.crud import deal as deal_crud
from app.utils import admin_required, high_level_required, get_current_user, get_info_from_tin

router = APIRouter(
	prefix = '/deals',
	tags=['Deals']
)

@router.get('/get-deals')
async def get_deals(db: db_depend, logRequest: Request, current_user= Depends(get_current_user)):
	response = await deal_crud.get_deals(db, logRequest, current_user)
	return response

@router.get('/get-deal')
async def get_deal(db: db_depend, deal_id : int , logRequest: Request, current_user = Depends(get_current_user)):
	response = await deal_crud.get_deal(db, deal_id, logRequest, current_user)
	return response

@router.post('/create-deal')
async def create_deal(db: db_depend, request: DealCreate, logRequest: Request, current_user = Depends(get_current_user)):
	response = await deal_crud.create_deal(db, request, logRequest, current_user)
	return response

@router.post('/update-deal')
async def update_deal(db: db_depend, request: DealUpdate, logRequest: Request, current_user= Depends(get_current_user)):
	response = await deal_crud.update_deal(db, request, logRequest, current_user)
	return response

@router.delete('/delete-deal')
async def delete_deal(db: db_depend, deal_id: int, logRequest: Request, current_user= Depends(get_current_user)):
	response = await deal_crud.delete_deal(db, deal_id, logRequest, current_user)
	return response

@router.post('/change-status-of-deal')
async def change_status_of_deal(db: db_depend, request: DealApprove, logRequest: Request, current_user= Depends(get_current_user)):
	response = await deal_crud.change_status_of_deal(db, request, logRequest, current_user)
	return response

@router.get('/get-deals-by-user')
async def get_deals_by_user(db: db_depend, logRequest: Request, current_user = Depends(get_current_user)):
	response = await deal_crud.get_deals_by_user(db, logRequest, current_user)
	return response

# THIS CODE FOR TRACKING TAX - IDENTIFICATION - NUMBER ( Use later)
# @router.get('/get-info-by-tin')
# async def get_info_by_tin(tin: str):
# 	response = await get_info_from_tin(tin)
# 	return response

@router.get('/get-deals-by-role')
async def get_deals_by_role(db: db_depend, role_id: int, logRequest: Request, current_user= Depends(get_current_user)):
	response = await deal_crud.get_deals_by_role(db, role_id, logRequest, current_user)
	return response

@router.get('/count-submitted-deals')
async def count_submitted_deals(db: db_depend, current_user = Depends(get_current_user)):
	response = await deal_crud.count_submitted_deals(db)
	return response