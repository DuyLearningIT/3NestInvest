from fastapi import APIRouter, Depends
from app.schemas import UserCreate, UserLogin, UserUpdate, UserChangePassword
from app.db import db_depend
from app.crud import user as user_crud
from app.utils import create_access_token, get_current_user, admin_required

router = APIRouter(
	prefix = '/users',
	tags=['Users']
)

# Admin required
@router.post('/create-user')
async def create_user(request: UserCreate, db: db_depend, admin=Depends(admin_required)):
	response = user_crud.create_user(db, request, admin)
	return response

# Admin required
@router.get('/get-users')
async def get_users(db: db_depend, admin= Depends(admin_required)):
	response =  user_crud.get_users(db, admin)
	return response

# User required
@router.get('/get-user')
async def get_user(db: db_depend, user_id : int, current_user= Depends(get_current_user)):
	response = user_crud.get_user(db, user_id)
	return response

@router.post('/login')
async def login(db: db_depend, request: UserLogin):
	response = user_crud.login(db, request)
	return response

# User required
@router.post('/update-user')
async def update_user(db: db_depend, request: UserUpdate, current_user = Depends(get_current_user)):
	response = user_crud.update_user(db, request)
	return response

# User required
@router.post('/change-password')
async def change_password(db: db_depend, user: UserChangePassword, current_user = Depends(get_current_user)):
	response = user_crud.change_passowrd(db, user)
	return response

# Admin required
@router.delete('/delete-user')
async def delete_user(db: db_depend, user_id : int, admin = Depends(admin_required)):
	response = user_crud.delete_user(db, user_id)
	return response

# User required
@router.get('/my-info')
async def get_my_info(db: db_depend, current_user = Depends(get_current_user)):
	response = user_crud.get_my_info(db, current_user)
	return response