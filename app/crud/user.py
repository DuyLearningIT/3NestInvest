from sqlalchemy.orm import Session, load_only
from app.models import User
from app.schemas import UserCreate, UserLogin, UserUpdate, UserChangePassword
from app.utils import hash_password, create_access_token, verify_password
from datetime import datetime

def get_users(db: Session):
	users = db.query(User).options(load_only(User.user_id, User.user_name, User.user_email, User.role)).all()
	return users

def get_user(db: Session, user_id : int):
	user = db.query(User).options(load_only(User.user_id, User.user_name, User.user_email, User.role)).filter(User.user_id == user_id).first()
	return user

def create_user(db: Session, user: UserCreate):
	check_email = db.query(User).filter(User.user_email == user.user_email).first()

	if check_email:
		return None

	hashed_pw = hash_password(user.password)

	db_user = User(
		user_name = user.user_name, 
		user_email = user.user_email,
		hashed_password = hashed_pw,
		role = user.role
	)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return {
		'user_id' : db_user.user_id,
		'user_name' : db_user.user_name,
		'role' : db_user.role,
		'user_email' : db_user.user_email
	}

def login(db: Session, user: UserLogin):
	check = db.query(User).filter(User.user_email == user.email).first()
	if check is None:
		return None
	
	if verify_password(user.password, check.hashed_password):
		return check
	return False

def update_user(db: Session, user: UserUpdate):
	check = db.query(User).filter(User.user_id == user.user_id).first()
	if check is None: 
		return None
	check.user_name = user.user_name or check.user_name
	check.company_name = user.company_name or check.company_name
	check.status = user.status or check.status
	check.phone = user.phone or check.phone
	check.updated_at = datetime.utcnow()
	check.updated_by = check.user_name

	db.commit()
	db.refresh(check)
	return {
		'data' : {
			'user_name' : check.user_name,
			'company_name' : check.company_name,
			'status' : check.status,
			'phone' : check.phone
		}
	}

def change_passowrd(db: Session, user: UserChangePassword):
	check = db.query(User).filter(User.user_id == user.user_id).first()
	if check is None:
		return None
	if verify_password(user.old_password, check.hashed_password):
		check.hashed_password = hash_password(user.new_password)
		db.commit()
		db.refresh(check)
		return True
	return False

def delete_user (db: Session, user_id: int):
	check = db.query(User).filter(User.user_id == user_id).first()
	if check is None:
		return None
	db.delete(check)
	db.commit()
	return True