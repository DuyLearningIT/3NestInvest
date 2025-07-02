from fastapi import APIRouter, Depends, Request
from app.schemas import UserCreate, UserLogin, UserUpdate, UserChangePassword
from app.db import db_depend
from app.crud import user as user_crud
from app.utils import create_access_token, get_current_user, admin_required
from pydantic import EmailStr

router = APIRouter(
	prefix = '/users',
	tags=['Users']
)

# Admin required
@router.post('/create-user')
async def create_user(request: UserCreate, db: db_depend, logRequest: Request, current_user = Depends(get_current_user)): 
	response = await user_crud.create_user(db, request, current_user, logRequest)
	return response

# Admin required
@router.get('/get-users')
async def get_users(db: db_depend, logRequest: Request, current_user = Depends(get_current_user)):
	response =  await user_crud.get_users(db, current_user, logRequest)
	return response

# User required
@router.get('/get-user')
async def get_user(db: db_depend, user_id : int, logRequest: Request, current_user= Depends(get_current_user)):
	response = await user_crud.get_user(db, user_id, current_user, logRequest)
	return response

@router.post('/login')
async def login(db: db_depend, request: UserLogin, logRequest: Request):
	response = await user_crud.login(db, request, logRequest)
	return response

# User required
@router.post('/update-user')
async def update_user(db: db_depend, request: UserUpdate, logRequest: Request, current_user = Depends(get_current_user)):
	response = await user_crud.update_user(db, request, current_user, logRequest)
	return response

# User required
@router.post('/change-password')
async def change_password(db: db_depend, user: UserChangePassword, logRequest: Request, current_user = Depends(get_current_user)):
	response = await user_crud.change_passowrd(db, user, current_user, logRequest)
	return response

# Admin required
@router.delete('/delete-user')
async def delete_user(db: db_depend, user_id : int, logRequest: Request, current_user = Depends(get_current_user)):
	response = await user_crud.delete_user(db, user_id, current_user, logRequest)
	return response

# User required
@router.get('/my-info')
async def get_my_info(db: db_depend, logRequest: Request, current_user = Depends(get_current_user)):
	response = await user_crud.get_my_info(db, current_user, logRequest)
	return response

@router.post('/reset-password')
async def reset_password(db: db_depend, email: EmailStr, phone: str):
	response = await user_crud.forgot_password(db, email, phone)
	return response

# Admin required
@router.get('/get-users-by-role')
async def get_users_by_role(db: db_depend, role: str, logRequest: Request, admin = Depends(admin_required)):
	response = await user_crud.get_users_by_role(db, role, logRequest, admin)
	return response