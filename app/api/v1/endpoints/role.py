from fastapi import APIRouter, Depends
from app.schemas import RoleCreate, RoleUpdate
from app.db import db_depend
from app.crud import role as role_crud
from app.utils import admin_required

router = APIRouter(
	prefix = '/roles',
	tags=['Roles']
)

@router.post('/create-role')
async def create_role(db: db_depend, request: RoleCreate):
	response = await role_crud.create_role(db, request)
	return response 

@router.post('/update-role')
async def update_role(db: db_depend, request: RoleUpdate):
	response = await role_crud.update_role(db, request)
	return response 

@router.get('/get-role')
async def get_role(db: db_depend, request_id):
	response = await role_crud.get_role(db, request_id)
	return response 

@router.get('/get-roles')
async def get_roles(db: db_depend):
	response = await role_crud.get_roles(db)
	return response 

@router.delete('/delete-role')
async def delete_role(db: db_depend, request_id):
	response = await role_crud.delete_role(db, request_id)
	return response 