from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserLogin, UserUpdate, UserChangePassword
from app.utils import hash_password, create_access_token, verify_password, conf, generate_random_password, get_internal_server_error, get_user_or_404
from datetime import datetime
from fastapi import HTTPException, status
from fastapi_mail import MessageSchema, MessageType, FastMail
from pydantic import EmailStr

async def get_users(db: Session, admin_required : dict):
	try:
		return {
			'mess' : 'Get all users successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : db.query(User).all()
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_user(db: Session, user_id : int):
	try:
		user = get_user_or_404(db, user_id)
		return {
			'mess': 'Get user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : user
		}
	except Exception as ex:
		return get_internal_server_error(ex)
	
async def create_user(db: Session, user: UserCreate, admin: dict):
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
		return get_internal_server_error(ex)

async def login(db: Session, user: UserLogin):
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
			'access_token' : create_access_token({'user_id' : check.user_id, 'user_name': check.user_name, 'user_email' : check.user_email, 'role' : check.role})
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def update_user(db: Session, user: UserUpdate):
	try:
		check = get_user_or_404(db, user.user_id)
		check.user_name = user.user_name or check.user_name
		check.company_name = user.company_name or check.company_name
		check.status = user.status
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
		return get_internal_server_error(ex)

async def change_passowrd(db: Session, user: UserChangePassword):
	try:
		check = get_user_or_404(db, user.user_id)
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
		return get_internal_server_error(ex)

async def delete_user (db: Session, user_id: int):
	try:
		check = get_user_or_404(db, user_id)
		db.delete(check)
		db.commit()
		return {
			'mess' : 'Delete user successfully !',
			'status_code': status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_my_info(db: Session, current_user: dict):
	try:
		user = get_user_or_404(db, current_user['user_id'])
		return{
			'mess' : 'Get user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : user
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def forgot_password(db: Session, email: EmailStr, phone: str):
    try:
        check = db.query(User).filter(User.user_email == email).first()
        if check is None:
            raise HTTPException(
                detail="User not found!",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        # Verify phone number
        if check.phone != phone.strip():
            raise HTTPException(
                detail="Phone doesn't match with your account!",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate new password and hash it
        new_password = generate_random_password()
        check.hashed_password = hash_password(new_password)
        db.commit()
        db.refresh(check)
		
		# Prepare content of email
        subject = "Password Reset for Your Account"
        body = f"""
        Dear {check.user_name or 'User'},
        
        Your password has been reset successfully. Your new password is:

        {new_password}

        Please log in with this password and change it immediately for security purposes.
        
        Regards,
        3Nest Invest Developer Team
        """
        message = MessageSchema(
            subject=subject,
            recipients=[email],  
            body=body,
            subtype=MessageType.plain
        )
        fm = FastMail(conf)
        await fm.send_message(message)

        return {
			"mess": "Password reset successfully. Check your email for the new password.",
			'status_code' : 200
		}

    except Exception as ex:
        return get_internal_server_error(ex)

# Admin required
async def get_users_by_role(db: Session, role: str):
	try:
		users = db.query(User).filter(User.role == role).all()
		return {
			'mess': 'Get users by role successfully !',
			'status_code': 200,
			'data' : users
		}
	except Exception as ex:
		return get_internal_server_error(ex)