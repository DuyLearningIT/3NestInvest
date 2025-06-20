from sqlalchemy.orm import Session
from app.models import User, Role
from app.schemas import UserCreate, UserLogin, UserUpdate, UserChangePassword
from app.utils import hash_password, create_access_token, verify_password, conf, generate_random_password, get_internal_server_error, get_user_or_404, log_activity
from datetime import datetime
from fastapi import HTTPException, status, Request
from fastapi_mail import MessageSchema, MessageType, FastMail
from pydantic import EmailStr
from app.utils.permission_checking import check_permission

async def get_users(db: Session, current_user: dict, request: Request):
	try:
		log_activity(
			db=db,
			request= request,
			user_id= current_user['user_id'],
			description= f"Get all users",
			target_type= "User"
		)
		return {
			'mess' : 'Get all users successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : db.query(User).all()
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_user(db: Session, user_id : int, current_user: dict, request: Request):
	try:
		log_activity(
			db=db,
			request= request,
			user_id= current_user['user_id'],
			description= f"Get user by id",
			target_type= f"Session: {datetime.now()}"
		)
		user = get_user_or_404(db, user_id)
		return {
			'mess': 'Get user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : user
		}
	except Exception as ex:
		return get_internal_server_error(ex)
	
async def create_user(db: Session, user: UserCreate, current_user: dict, request: Request):
	try:
		
		permission = await check_permission(db, 'manage', 'user', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
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
			role_id = user.role_id,
			company_name = user.company_name
		)
		db.add(db_user)
		db.commit()
		db.refresh(db_user)
		log_activity(
			db=db,
			request= request,
			user_id= current_user['user_id'],
			description= f"Create an user",
			target_type= "User"
		)
		return {
			'mess' : 'Create user successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data' : {
				'user_id' : db_user.user_id,
				'user_name' : db_user.user_name,
				'company_name' : db_user.company_name,
				'role_id' : db_user.role_id,
				'user_email' : db_user.user_email
			}
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def login(db: Session, user: UserLogin, request: Request):
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
		role = db.query(Role).filter(Role.role_id== check.role_id).first()
		log_activity(
			db=db,
			request= request,
			user_id= check.user_id,
			description= f"User logged in",
			target_type= "User"
		)
		return {
			'mess' : 'Login successfully !',
			'status_code': status.HTTP_200_OK,
			'data' : { 
				'role' : check.role,
				'user_name' : check.user_name
			},
			'access_token' : create_access_token({'user_id' : check.user_id, 'user_name': check.user_name, 'user_email' : check.user_email, 'role' : role.role_name, 'role_id' : role.role_id})
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def update_user(db: Session, user: UserUpdate, current_user: dict, request: Request):
	try:
		check_user = user.user_id == current_user['user_id']
		permission = await check_permission(db, 'manage', 'user', current_user['role_id'])
		if permission == False and check_user == False:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		check = get_user_or_404(db, user.user_id)
		check.user_name = user.user_name or check.user_name
		check.company_name = user.company_name or check.company_name
		check.status = user.status or check.status
		check.phone = user.phone or check.phone
		check.updated_at = datetime.now()
		check.updated_by = check.user_name

		db.commit()
		db.refresh(check)
		log_activity(
			db=db,
			request= request,
			user_id= current_user['user_id'],
			description= "Update user",
			target_type= "User"
		)
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

async def change_passowrd(db: Session, user: UserChangePassword, request: Request):
	try:
		check_user = user.user_id == current_user['user_id']
		permission = await check_permission(db, 'manage', 'user', current_user['role_id'])
		if permission == False and check_user == False:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		check = get_user_or_404(db, user.user_id)
		if not verify_password(user.old_password, check.hashed_password):
			raise HTTPException(
				detail= 'Email or password was wrong !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		check.hashed_password = hash_password(user.new_password)
		db.commit()
		db.refresh(check)
		log_activity(
			db=db,
			request= request,
			user_id= current_user['user_id'],
			description= "Change password",
			target_type= "User"
		)
		return {
			'mess' : 'Change password successfully !',
			'status_code' : status.HTTP_200_OK
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def delete_user (db: Session, user_id: int, current_user: dict, request: Request):
	try:
		permission = await check_permission(db, 'manage', 'user', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		check = get_user_or_404(db, user_id)
		db.delete(check)
		db.commit()
		log_activity(
			db=db,
			request= request,
			user_id= current_user['user_id'],
			description= "Delete user",
			target_type= "User"
		)
		return {
			'mess' : 'Delete user successfully !',
			'status_code': status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_my_info(db: Session, current_user: dict, request: Request):
	try:
		user = get_user_or_404(db, current_user['user_id'])
		log_activity(
			db=db,
			request= request,
			user_id= current_user['user_id'],
			description= "Get user's information",
			target_type= "User"
		)
		return{
			'mess' : 'Get user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : {
				'user_name': user.user_name,
				'user_email': user.user_email,
				'company_name': user.company_name,
				'created_at' : user.created_at,
				'phone': user.phone
			}
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
async def get_users_by_role(db: Session, role_id: int, request: Request):
	try:
		permission = await check_permission(db, 'manage', 'user', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		users = db.query(User).filter(User.role_id == role_id).all()
		log_activity(
			db=db,
			request= request,
			user_id= current_user['user_id'],
			description= "Get users by role",
			target_type= "User"
		)
		return {
			'mess': 'Get users by role successfully !',
			'status_code': 200,
			'data' : users
		}
	except Exception as ex:
		return get_internal_server_error(ex)