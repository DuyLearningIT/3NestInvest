from sqlalchemy.orm import Session
from app.models import Order, OrderDetails, User, Product, Deal
from app.schemas import DealUpdate, DealCreate, DealApprove
from fastapi import Depends
from datetime import datetime
from fastapi import HTTPException, status
from app.utils import get_internal_server_error, get_deal_or_404, get_user_or_404

# High-level required
async def get_deals(db: Session):
	try:
		return {
			'mess' : 'Get all deals successfully !',
			'data' : db.query(Deal).filter(Deal.status != 'draft').all(),
			'status_code' : status.HTTP_200_OK
		}
	except Exception as ex:
		raise HTTPException(
			detail = f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

async def get_deal(db: Session, deal_id : int):
	try:
		deal = get_deal_or_404(db, deal_id)
		user = get_user_or_404(db, deal.user_id)
		return {
			'mess' : 'Get deal successfully !',
			'data' : {
				'deal' : deal,
				'role' : user.role
			},
			'status_code' : status.HTTP_200_OK
		}
	except Exception as ex:
		return get_internal_server_error(ex)

# User required
async def create_deal(db: Session, request: DealCreate, current_user : dict):
	try:
		user = get_user_or_404(db, current_user['user_id'])
		check_deal = db.query(Deal).filter(Deal.tax_indentification_number == request.tax_indentification_number, Deal.status == 'approved').first()
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
		return get_internal_server_error(ex)

# User required
async def update_deal(db: Session, request: DealUpdate, current_user: dict):
	try:
		user = get_user_or_404(db, current_user['user_id'])
		deal = get_deal_or_404(db, request.deal_id)

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
		return get_internal_server_error(ex)

# User required
async def delete_deal(db: Session, deal_id : int, current_user: dict):
	try:
		deal = get_deal_or_404(db, deal_id)
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
		return get_internal_server_error(ex)

# High-level required 
async def change_status_of_deal(db: Session, request : DealApprove):
	try:
		deal = get_deal_or_404(db, request.deal_id)
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
		return get_internal_server_error(ex)

# User required
async def get_deals_by_user(db: Session, current_user: dict):
	try:
		user = get_user_or_404(db, current_user['user_id'])
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
	
# Admin required
async def get_deals_by_role(db: Session, role: str):
	try:
		deals = db.query(Deal).all()
		ds = []
		for deal in deals:
			user = get_user_or_404(db, deal.user_id)
			if user.role == role:
				ds.append(deal)
		return {
			'mess': 'Get deals by role successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : ds
		}
	except Exception as ex:
		return get_internal_server_error(ex)