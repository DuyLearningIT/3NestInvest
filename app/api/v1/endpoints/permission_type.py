from fastapi import APIRouter, Depends
from app.schemas import PermissionTypeCreate, PermissionTypeUpdate
from app.db import db_depend
from app.crud import permission_type as permission_type_crud
from app.utils import admin_required, high_level_required, get_current_user, get_info_from_tin

router = APIRouter(
	prefix = '/permission_types',
	tags=['Permission Types']
)

# @router.post('/create-permission-type')
# async def create_permission_type(db: db_depend, request : PermissionTypeCreate):
# 	response = await permission_type_crud.create_permission_type(db, request)
# 	return response

# @router.post('/update-permission-type')
# async def update_permission_type(db: db_depend, request: PermissionTypeUpdate):
# 	response = await permission_type_crud.update_permission_type(db, request)
# 	return response

@router.get('/get-permission-types')
async def get_permission_types(db: db_depend):
	response = await permission_type_crud.get_permission_types(db)
	return response

@router.get('/get-permission-type')
async def get_permission_type(db: db_depend, request_id: int):
	response = await permission_type_crud.get_permission_type(db, request_id)
	return response

# @router.delete('/delete-permission-type')
# async def delete_permission_type(db: db_depend, request_id : int):
# 	response = await permission_type_crud.delete_permission_type(db, request_id)
# 	return response