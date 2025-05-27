from sqlalchemy.orm import Session
from app.models import UserRequest
from app.schemas import CreateRequest, UpdateRequest

def create_request(db: Session, request : CreateRequest):
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
			'status_code' : 201,
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong : {ex}',
			'status_code' : 500
		}
def update_request(db: Session, request: UpdateRequest):
	try:
		check = db.query(UserRequest).filter(UserRequest.request_id == request.request_id).first()
		if check is None:
			return {
				'mess' : 'Request not found !',
				'status_code': 404
			}
		check.user_name = request.user_name or check.user_name
		check.user_email = request.user_email or check.user_email
		check.company_name = request.company_name or check.company_name
		check.phone = request.phone or check.phone 
		check.status = request.status or check.status

		db.commit()
		return {
			'mess' : 'Update request successfully !',
			'status_code' : 200
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong : {ex}',
			'status_code' : 500
		}
def get_request(db: Session, request_id):
	try: 
		request = db.query(UserRequest).filter(UserRequest.request_id == request_id).first()
		if request is None:
			return {
				'mess' : 'Request not found !',
				'status_code' : 404
			}
		return {
			'mess' : 'Get request successfully !',
			'status_code': 200,
			'data' : request
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong : {ex}',
			'status_code' : 500
		}

# Admin required
def get_requests(db: Session, admin: dict):
	try:
		return {
			'mess': 'Get all requests successfully !',
			'status_code' : 200,
			'data' : db.query(UserRequest).all()
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong : {ex}',
			'status_code' : 500
		}

# Admin required
def delete_request(db: Session, request_id:int, admin: dict):
	try: 
		request = db.query(UserRequest).filter(UserRequest.request_id == request_id).first()
		if request is None:
			return {
				'mess' : 'Request not found !',
				'status_code' : 404
			}
		db.delete(request)
		db.commit()
		return {
			'mess' : 'Get request successfully !',
			'status_code': 204
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong : {ex}',
			'status_code' : 500
		}