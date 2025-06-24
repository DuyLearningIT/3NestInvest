from fastapi import APIRouter, Depends, Request
from app.schemas import ChangeCreate, ChangeUpdate
from app.db import db_depend
from app.crud import change_management as change_crud
from app.utils import admin_required, get_current_user

router = APIRouter(
	prefix = '/change',
	tags=['Change Management']
)

@router.get('/get-changes')
async def get_changes(db: db_depend, admin = Depends(admin_required)):
	response = await change_crud.get_changes(db)
	return response 

@router.get('/get-change')
async def get_change(db: db_depend, request_id: int, admin = Depends(admin_required)):
	response = await change_crud.get_change(db, request_id)
	return response 

@router.post('/create-change')
async def create_change(db: db_depend, request: ChangeCreate, admin = Depends(admin_required)):
	response = await change_crud.create_change_management(db, request)
	return response 

@router.post('/update-change')
async def update_change(db: db_depend, request: ChangeUpdate, admin = Depends(admin_required)):
	response = await change_crud.update_change(db, request)
	return response

@router.delete('/delete-change')
async def delete_change(db: db_depend, request_id: int, admin = Depends(admin_required)):
	response = await change_crud.delete_change(db, request_id)
	return response