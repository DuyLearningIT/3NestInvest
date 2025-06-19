from fastapi import APIRouter, Depends, Request
from app.schemas import RoleCreate, RoleUpdate
from app.db import db_depend
from app.crud import role as role_crud
from app.utils import admin_required, get_current_user

router = APIRouter(
	prefix = '/roles',
	tags=['Roles']
)

@router.post('/create-role')
async def create_role(db: db_depend, request: RoleCreate, logRequest: Request, current_user = Depends(get_current_user)):
	response = await role_crud.create_role(db, request, logRequest, current_user)
	return response 

@router.post('/update-role')
async def update_role(db: db_depend, request: RoleUpdate, logRequest: Request, current_user = Depends(get_current_user)):
	response = await role_crud.update_role(db, request, logRequest, current_user)
	return response 

@router.get('/get-role')
async def get_role(db: db_depend, request_id: int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await role_crud.get_role(db, request_id, logRequest, current_user)
	return response 

@router.get('/get-roles')
async def get_roles(db: db_depend, logRequest: Request, current_user = Depends(get_current_user)):
	response = await role_crud.get_roles(db, logRequest, current_user)
	return response 

@router.delete('/delete-role')
async def delete_role(db: db_depend, request_id: int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await role_crud.delete_role(db, request_id, logRequest, current_user)
	return response