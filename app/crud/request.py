from sqlalchemy.orm import Session
from app.models import UserRequest
from app.schemas import CreateRequest, UpdateRequest
from fastapi import HTTPException, status
from app.utils import get_internal_server_error, get_request_or_404
from app.utils.permission_checking import check_permission


async def create_request(db: Session, request : CreateRequest):
	try:
		new_request = UserRequest(
			user_name = request.user_name,
			user_email = request.user_email,
			company_name = request.company_name,
			phone = request.phone
		)
		db.add(new_request)
		db.commit()
		db.refresh(new_request)
		return{
			'mess' : 'Create request successfully !',
			'status_code' : status.HTTP_201_CREATED,
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def update_request(db: Session, request: UpdateRequest):
	try:
		check = get_request_or_404(db, request.request_id)
		check.user_name = request.user_name or check.user_name
		check.user_email = request.user_email or check.user_email
		check.company_name = request.company_name or check.company_name
		check.phone = request.phone or check.phone 
		check.status = request.status or check.status

		db.commit()
		return {
			'mess' : 'Update request successfully !',
			'status_code' : status.HTTP_200_OK
		}
	except Exception as ex:
		return get_internal_server_error(ex)


async def get_request(db: Session, request_id):
	try: 
		request = get_request_or_404(db, request_id)
		return {
			'mess' : 'Get request successfully !',
			'status_code': status.HTTP_200_OK,
			'data' : request
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong : {ex}',
			'status_code' : 500
		}

async def get_requests(db: Session):
	try:
		return {
			'mess': 'Get all requests successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : db.query(UserRequest).all()
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def delete_request(db: Session, request_id:int):
	try: 
		request = get_request_or_404(db, request_id)
		db.delete(request)
		db.commit()
		return {
			'mess' : 'Delete request successfully !',
			'status_code': status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		return get_internal_server_error(ex)