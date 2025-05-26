from fastapi import APIRouter, Depends
from app.schemas import UserCreate, UserLogin, UserUpdate, UserChangePassword
from app.db import db_depend
from app.crud import user as user_crud
from app.utils import create_access_token, get_current_user

router = APIRouter(
	prefix = '/users',
	tags=['Users']
)

@router.post('/create-user')
async def create_user(request: UserCreate, db: db_depend):
	try:
		data = user_crud.create_user(db, request)
		if data is None:
			return {
				'mess' : 'Email has already used ! Please try another one!',
				'status_code' : 404
			}
		return {
			'mess' : 'Created user successfully!',
			'status_code' : 201,
			'data' : data
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}

@router.get('/get-users')
async def get_users(db: db_depend):
	try:
		data = user_crud.get_users(db)
		return {
			'mess' : 'Get all users successfully !',
			'data' : data,
			'status_code' : 200
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}

@router.get('/get-user')
async def get_user(db: db_depend, user_id : int):
	try:
		data = user_crud.get_user(db, user_id)
		if data is None:
			return {
				'mess' : 'User not found !',
				'status_code' : 404
			}
		return {
			'mess' : 'Get user successfully !',
			'data' : data,
			'status_code' : 200
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}

@router.post('/login')
async def login(db: db_depend, request: UserLogin):
	response = user_crud.login(db, request)
	return response

@router.post('/update-user')
async def update_user(db: db_depend, request: UserUpdate):
	try:
		data = user_crud.update_user(db, request)
		if data is None: 
			return {
				'mess' : 'User not found !',
				'status_code' : 404
			}
		return{
			'mess' : 'Update user successfully !',
			'status_code' : 200,
			'data' : data
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}

@router.post('/change-password')
async def change_password(db: db_depend, user: UserChangePassword):
	try:
		check = user_crud.change_passowrd(db, user)
		if check == None:
			return{
				'mess' : 'User not found !',
				'status_code' : 404
			}
		elif check == False:
			return{
				'mess' : 'Password was wrong ! Please try again !',
				'status_code' : 400
			}
		return {
			'mess' : 'Change password successfully !',
			'status_code' : 200
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}

@router.delete('/delete-user')
async def delete_user(db: db_depend, user_id : int):
	try:
		check = user_crud.delete_user(db, user_id)
		if check is None:
			return {
				'mess' : 'User not found !',
				'status_code' : 404
			}
		return{
			'mess' : 'Delete user successfully !',
			'status_code' : 204
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}
	
@router.get('/my-info')
async def get_my_info(db: db_depend, current_user = Depends(get_current_user)):
	response = user_crud.get_my_info(db, current_user)
	return response