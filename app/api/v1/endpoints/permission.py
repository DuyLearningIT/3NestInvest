from fastapi import APIRouter, Depends
from app.schemas import PermissionCreate, PermissionUpdate
from app.db import db_depend
from app.crud import permission as permission_crud
from app.utils import admin_required, high_level_required, get_current_user, get_info_from_tin

router = APIRouter(
	prefix = '/permissions',
	tags=['Permissions']
)

# @router.post('/create-permission')
# async def create_permission(db: db_depend, request: PermissionCreate):
# 	response = await permission_crud.create_permission(db, request)
# 	return response

# @router.post('/update-permission')
# async def update_permission(db: db_depend, request: PermissionUpdate):
# 	response = await permission_crud.update_permission(db, request)
# 	return response

@router.get('/get-permission')
async def get_permission(db: db_depend, request_id):
	response = await permission_crud.get_permission(db, request_id)
	return response

@router.get('/get-permissions')
async def get_permissions(db: db_depend):
	response = await permission_crud.get_permissions(db)
	return response 

@router.get('/get-permissions-by-type')
async def get_permissions_by_type(db: db_depend, request_id):
	response = await permission_crud.get_permissions_by_type(db, request_id)
	return response 

# @router.delete('/delete-permission')
# async def delete_permission(db: db_depend, request_id):
# 	response = await permission_crud.delete_permission(db, request_id)
# 	return repsonse 
