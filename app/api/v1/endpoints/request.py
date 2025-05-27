from fastapi import APIRouter, Depends
from app.schemas import CreateRequest, UpdateRequest
from app.db import db_depend
from app.crud import request as request_crud
from app.utils import admin_required

router = APIRouter(
	prefix = '/user-request',
	tags=['UserRequests']
)

@router.get('/get-request')
async def get_request(db: db_depend, request_id):
	response = request_crud.get_request(db, request_id)
	return response

# Admin required
@router.get('/get-requests')
async def get_requests(db: db_depend, admin= Depends(admin_required)):
	response = request_crud.get_requests(db, admin)
	return response

@router.post('/create-request')
async def create_request(db: db_depend, request: CreateRequest):
	response = request_crud.create_request(db, request)
	return response

@router.post('/update-request')
async def update_request(db: db_depend, request: UpdateRequest):
	response = request_crud.update_request(db, request)
	return response 

# Admin required
@router.delete('/delete-request')
async def delete_request(db: db_depend, request_id: int, admin= Depends(admin_required)):
	response = request_crud.delete_request(db, request_id, admin)
	return response