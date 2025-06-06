from sqlalchemy.orm import Session
from app.models import Order, OrderDetails, User, Product, Deal
from app.schemas import DealUpdate, DealCreate, DealApprove
from fastapi import Depends
from datetime import datetime
from fastapi import HTTPException, status

# High-level required
async def get_deals(db: Session):
	try:
		return {
			'mess' : 'Get all deals successfully !',
			'data' : db.query(Deal).all(),
			'status_code' : status.HTTP_200_OK
		}
	except Exception as ex:
		raise HTTPException(
			detail = f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

async def get_deal(db: Session, deal_id : int):
	try:
		deal = db.query(Deal).filter(Deal.deal_id == deal_id).first()
		if deal is None:
			raise HTTPException(
				detail = 'Deal not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		
		return {
			'mess' : 'Get deal successfully !',
			'data' : deal,
			'status_code' : status.HTTP_200_OK
		}
	except Exception as ex:
		raise HTTPException(
			detail = f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# User required
async def create_deal(db: Session, request: DealCreate, current_user : dict):
	try:
		user = db.query(User).filter(User.user_id == current_user['user_id']).first()
		if user is None:
			raise HTTPException(
				detail = 'User not found !',
				status_code= status.HTTP_404_NOT_FOUND
			)
		check_deal = db.query(Deal).filter(Deal.tax_indentification_number == request.tax_indentification_number and Deal.status == 'approved').first()
		if check_deal:
			raise HTTPException(
				detail = 'Deal has already existed',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		new_deal = Deal(
			deal_type=request.deal_type,
			description=request.description,
			user_id= user.user_id,
			tax_indentification_number=request.tax_indentification_number,
			customer_name=request.customer_name,
			domain_name=request.domain_name,
			contact_name=request.contact_name,
			contact_email=request.contact_email,
			contact_phone=request.contact_phone,
			status=request.status,
			address=request.address,
			billing_address=request.billing_address,
			created_by = user.user_name
		)
		db.add(new_deal)
		db.commit()
		db.refresh(new_deal)
		return{
			'mess' : 'Create deal successfully !',
			'status_code': status.HTTP_201_CREATED,
			'data': new_deal
		}
	except Exception as ex:
		db.rollback()
		raise HTTPException (
			detail = f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# User required
async def update_deal(db: Session, request: DealUpdate, current_user: dict):
	try:
		user = db.query(User).filter(User.user_id == current_user['user_id']).first()
		if user is None:
			raise HTTPException(
				detail='User not found!',
				status_code=status.HTTP_404_NOT_FOUND
			)

		deal = db.query(Deal).filter(Deal.deal_id == request.deal_id).first()
		if deal is None:
			raise HTTPException(
				detail='Deal not found!',
				status_code=status.HTTP_404_NOT_FOUND
			)
		if deal.user_id != user.user_id:
			raise HTTPException(
				detail = 'Cannot revise the order which is not your own !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		deal.deal_type = request.deal_type or deal.deal_type
		deal.description = request.description or deal.description
		deal.tax_indentification_number = request.tax_indentification_number or deal.tax_indentification_number
		deal.customer_name = request.customer_name or deal.customer_name
		deal.domain_name = request.domain_name or deal.domain_name
		deal.contact_name = request.contact_name or deal.contact_name
		deal.contact_email = request.contact_email or deal.contact_email
		deal.contact_phone = request.contact_phone or deal.contact_phone
		deal.status = request.status or deal.status
		deal.address = request.address or deal.address
		deal.billing_address = request.billing_address or deal.billing_address
		deal.updated_at = datetime.utcnow()
		deal.updated_by = user.user_name
        
		db.commit()
		db.refresh(deal)
		return {
			'mess': 'Update deal successfully!',
			'status_code': status.HTTP_200_OK,
			'data': deal
		}

	except Exception as ex:
		db.rollback()
		raise HTTPException(
			detail = f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# User required
async def delete_deal(db: Session, deal_id : int, current_user: dict):
	try:
		deal = db.query(Deal).filter(Deal.deal_id == deal_id).first()
		if deal is None:
			raise HTTPExeption (
				detail = 'Deal not found !',
				status_code= status.HTTP_404_NOT_FOUND
			)
		if deal.user_id != current_user['user_id']:
			raise HTTPException(
				detail = 'Cannot remove deal which is not your own !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		db.delete(deal)
		db.commit()
		return {
			'mess' : 'Delete deal successfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		db.rollback()
		raise HTTPException(
			detail = f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# High-level required 
def change_status_of_deal(db: Session, request : DealApprove):
	try:
		deal = db.query(Deal).filter(Deal.deal_id == request.deal_id).first()
		if deal is None:
			raise HTTPExeption (
				detail = 'Deal not found !',
				status_code= status.HTTP_404_NOT_FOUND
			)
		deal.status = request.status or deal.status
		db.commit()
		db.refresh(deal)
		return {
			'mess' : 'Change the status of deal successfully !',
			'status_code' : status.HTTP_200_OK,
			'data': deal
		}
	except Exception as ex:
		db.rollback()
		raise HTTPException(
			detail = f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# User required
async def get_deals_by_user(db: Session, current_user: dict):
	try:
		user = db.query(User).filter(User.user_id == current_user['user_id']).first()
		if user is None:
			raise HTTPException(
				detai = 'User not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		return {
			'mess' : 'Get deals by user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : db.query(Deal).filter(Deal.user_id == user.user_id).all()
		}
	except Exception as ex:
		raise HTTPException(
			detail = f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)