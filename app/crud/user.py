from sqlalchemy.orm import Session, load_only
from app.models import User
from app.schemas import UserCreate, UserLogin, UserUpdate, UserChangePassword
from app.utils import hash_password, create_access_token, verify_password
from datetime import datetime
from fastapi import HTTPException, status

def get_users(db: Session, admin_required : dict):
	try:
		return {
			'mess' : 'Get all users successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : db.query(User).options(load_only(User.user_id, User.user_name, User.user_email, User.role, User.company_name, User.phone)).all()
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def get_user(db: Session, user_id : int):
	try:
		user = db.query(User).options(load_only(User.user_id, User.user_name, User.user_email, User.role)).filter(User.user_id == user_id).first()
		if user is None:
			raise HTTPException(
				detail= 'User not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		return {
			'mess': 'Get user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : user
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)
	
def create_user(db: Session, user: UserCreate, admin: dict):
	try:
		check_email = db.query(User).filter(User.user_email == user.user_email).first()

		if check_email:
			raise HTTPException(
			detail= 'Email has already existed !',
			status_code = status.HTTP_400_BAD_REQUEST
		)

		hashed_pw = hash_password(user.password)

		db_user = User(
			user_name = user.user_name, 
			user_email = user.user_email,
			hashed_password = hashed_pw,
			role = user.role,
			company_name = user.company_name
		)
		db.add(db_user)
		db.commit()
		db.refresh(db_user)
		return {
			'mess' : 'Create user successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data' : {
				'user_id' : db_user.user_id,
				'user_name' : db_user.user_name,
				'company_name' : db_user.company_name,
				'role' : db_user.role,
				'user_email' : db_user.user_email
				}
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def login(db: Session, user: UserLogin):
	try:
		check = db.query(User).filter(User.user_email == user.user_email).first()
		if check is None:
			raise HTTPException(
				detail= 'Email not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		if not verify_password(user.password, check.hashed_password):
			raise HTTPException(
				detail= 'Email or password was wrong !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		return{
			'mess' : 'Login successfully !',
			'status_code': status.HTTP_200_OK,
			'data' : { 
				'role' : check.role,
				'user_name' : check.user_name
			},
			'access_token' : create_access_token({'user_id' : check.user_id, 'user_email' : check.user_email, 'role' : check.role})
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def update_user(db: Session, user: UserUpdate, current_user: dict):
	try:
		check = db.query(User).filter(User.user_id == user.user_id).first()
		if check is None: 
			raise HTTPException(
			detail= 'User not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
		check.user_name = user.user_name or check.user_name
		check.company_name = user.company_name or check.company_name
		check.status = user.status or check.status
		check.phone = user.phone or check.phone
		check.updated_at = datetime.utcnow()
		check.updated_by = check.user_name

		db.commit()
		db.refresh(check)
		return {
			'mess' : 'Update user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : {
				'user_name' : check.user_name,
				'company_name' : check.company_name,
				'status' : check.status,
				'phone' : check.phone
			}
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def change_passowrd(db: Session, user: UserChangePassword):
	try:
		check = db.query(User).filter(User.user_id == user.user_id).first()
		if check is None:
			raise HTTPException(
				detail= 'User not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		if not verify_password(user.old_password, check.hashed_password):
			raise HTTPException(
				detail= 'Email or password was wrong !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		check.hashed_password = hash_password(user.new_password)
		db.commit()
		db.refresh(check)
		return {
			'mess' : 'Change password successfully !',
			'status_code' : status.HTTP_200_OK
		}
	except Exception as ex:
		raise HTTPException(
			detail= f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def delete_user (db: Session, user_id: int):
	try:
		check = db.query(User).filter(User.user_id == user_id).first()
		if check is None:
			raise HTTPException(
			detail= 'User not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
		db.delete(check)
		db.commit()
		return {
			'mess' : 'Delete user successfully !',
			'status_code': status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def get_my_info(db: Session, current_user: dict):
	try:
		user = db.query(User).filter(User.user_id == current_user['user_id']).first()
		if check is None:
			raise HTTPException(
			detail= 'User not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
		return{
			'mess' : 'Get user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : user
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)