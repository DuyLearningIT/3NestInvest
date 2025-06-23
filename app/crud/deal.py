from sqlalchemy.orm import Session, joinedload
from app.models import Order, OrderDetails, User, Product, Deal
from app.schemas import DealUpdate, DealCreate, DealApprove
from fastapi import Depends, Request
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi import HTTPException, status
from app.utils import get_internal_server_error, get_deal_or_404, get_user_or_404, log_activity
from app.utils.permission_checking import check_permission

async def get_deals(db: Session, logRequest: Request, current_user:dict):
	try:
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Get all deals",
			target_type= "Deal"
		)
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

async def get_deal(db: Session, deal_id : int, logRequest: Request, current_user: dict):
	try:
		deal = get_deal_or_404(db, deal_id)
		user = get_user_or_404(db, deal.user_id)
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Get deal by id",
			target_type= "Deal"
		)
		return {
			'mess' : 'Get deal successfully !',
			'data' : {
				'deal' : {
					'deal_id': deal.deal_id,
					'deal_type': deal.deal_type,
					'user_id': deal.user_id,
					'contact_name': deal.contact_name,
					'contact_phone': deal.contact_phone,
					'contact_email': deal.contact_email,
					'customer_name' : deal.customer_name,
					'tax_identification_number': deal.tax_indentification_number,
					'address': deal.address,
					'billing_address': deal.billing_address,
					'created_at': deal.created_at.isoformat() if deal.created_at else None,
					'status': deal.status
				},
				'role' : user.role
			},
			'status_code' : status.HTTP_200_OK
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def create_deal(db: Session, request: DealCreate, logRequest: Request, current_user : dict):
	try:
		permission = await check_permission(db, 'manage', 'deal', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		user = get_user_or_404(db, current_user['user_id'])
		check_deal = db.query(Deal).filter(Deal.tax_indentification_number == request.tax_indentification_number, Deal.status == 'approved').first()
		if check_deal:
			raise HTTPException(
				detail = 'Deal has already existed',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		new_deal = Deal(
			deal_type=request.deal_type,
			deal_description=request.deal_description,
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
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Create a deal",
			target_type= "Deal"
		)
		return{
			'mess' : 'Create deal successfully !',
			'status_code': status.HTTP_201_CREATED,
			'data': {
				'deal_id' : new_deal.deal_id
			}
		}
	except Exception as ex:
		db.rollback()
		return get_internal_server_error(ex)

async def update_deal(db: Session, request: DealUpdate, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'deal', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		user = get_user_or_404(db, current_user['user_id'])
		deal = get_deal_or_404(db, request.deal_id)

		if deal.user_id != user.user_id:
			raise HTTPException(
				detail = 'Cannot revise the order which is not your own !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		deal.deal_type = request.deal_type or deal.deal_type
		deal.deal_description = request.deal_description or deal.deal_description
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
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Update a deal",
			target_type= "Deal"
		)
		return {
			'mess': 'Update deal successfully!',
			'status_code': status.HTTP_200_OK,
			'data': deal
		}

	except Exception as ex:
		db.rollback()
		return get_internal_server_error(ex)

async def delete_deal(db: Session, deal_id : int, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'deal', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		deal = get_deal_or_404(db, deal_id)
		if deal.user_id != current_user['user_id']:
			raise HTTPException(
				detail = 'Cannot remove deal which is not your own !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		db.delete(deal)
		db.commit()
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Delete a deal",
			target_type= "Deal"
		)
		return {
			'mess' : 'Delete deal successfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		db.rollback()
		return get_internal_server_error(ex)

async def change_status_of_deal(db: Session, request : DealApprove, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'review', 'deal', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		deal = get_deal_or_404(db, request.deal_id)
		deal.status = request.status or deal.status
		deal.reason = request.reason or deal.reason
		db.commit()
		db.refresh(deal)
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Review a deal",
			target_type= "Deal"
		)
		return {
			'mess' : 'Change the status of deal successfully !',
			'status_code' : status.HTTP_200_OK,
			'data': deal
		}
	except Exception as ex:
		db.rollback()
		return get_internal_server_error(ex)

async def get_deals_by_user(db: Session, logRequest: Request, current_user: dict):
	try:
		user = get_user_or_404(db, current_user['user_id'])
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Get all deals  by user",
			target_type= "Deal"
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
	
async def get_deals_by_role(db: Session, role_id: int, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'deal', current_user['role_id'])
		if not permission:
			return {
				'mess': "You don't have permission for accessing this function!",
				'status_code': status.HTTP_403_FORBIDDEN
			}
		deals = db.query(Deal).join(User).filter(User.role_id == role_id).all()

		log_activity(
			db=db,
			request=logRequest,
			user_id=current_user['user_id'],
			activity_description="Get all deals by role",
			target_type="Deal"
		)

		return {
			'mess': 'Get deals by role successfully!',
			'status_code': status.HTTP_200_OK,
			'data': [
				{
					'deal_id': deal.deal_id,
					'deal_type': deal.deal_type,
					'user_id': deal.user_id,
					'contact_name': deal.contact_name,
					'contact_phone': deal.contact_phone,
					'contact_email': deal.contact_email,
					'customer_name' : deal.customer_name,
					'tax_identification_number': deal.tax_indentification_number,
					'address': deal.address,
					'billing_address': deal.billing_address,
					'created_at': deal.created_at.isoformat() if deal.created_at else None,
					'status': deal.status
				}
				for deal in deals
			]
		}																
	except Exception as ex:
		return get_internal_server_error(ex)