from sqlalchemy.orm import Session
from app.models import Order, OrderDetails, User, Product, Deal
from app.schemas import OrderCreate, OrderUpdate, OrderApprove
from fastapi import Depends
from datetime import datetime
from fastapi import HTTPException, status
from app.utils import get_internal_server_error, get_deal_or_404, get_user_or_404, get_product_or_404, get_order_or_404

# User required
async def create_order(db: Session, order : OrderCreate, current_user: dict):
	try:
		user = get_user_or_404(db, current_user['user_id'])
		check_deal = get_deal_or_404(db, order.deal_id)
		if check_deal.user_id != user.user_id:
			raise HTTPException(
				detail = 'Cannot add the order based on the deal which is not your own !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		
		db_order = Order(
			deal_id = order.deal_id,
			order_title=order.order_title,
			created_by=user.user_name,
			status = order.status
		)
		db.add(db_order)
		db.commit()
		db.refresh(db_order)

		total_budget = 0
		initial_price = 0
		for detail in order.details:
			product = get_product_or_404(db, detail.product_id)

			if current_user['role'] == 'channels':
				initial_price = product.channel_cost * detail.quantity
			else:
				if detail.price_for_customer < product.maximum_discount_price:
					raise HTTPException(
						detail= 'Price for customer cannot be lower than minimum price !',
						status_code = status.HTTP_400_BAD_REQUEST
					)
				initial_price = detail.price_for_customer * detail.quantity

			prices = []
			# Increase the price through each year of contract duration
			for i in range(detail.service_contract_duration):
				prices.append(initial_price * (1.05 ** i)) 

			final_price = sum(prices)

			db_detail = OrderDetails(
				order_id=db_order.order_id,
				product_id=detail.product_id,
				quantity=detail.quantity,
				price_for_customer =detail.price_for_customer, # if the role is channels -> then don't care this field
				service_contract_duration = detail.service_contract_duration,
				final_price=final_price
			) 
			# Calculate all the total budget
			total_budget += final_price
			db.add(db_detail)

		db_order.total_budget = total_budget
		db.commit()

		return {
			'mess': 'Create order successfully!',
			'status_code': status.HTTP_201_CREATED,
			'data': db_order
		}

	except Exception as ex:
		db.rollback()
		return get_internal_server_error(ex)

# User required
async def get_order(db: Session, order_id : int):
	try:
		order = get_order_or_404(db, order_id)
		return {
			'mess' : 'Get order successfully !',
			'status_code' : status.HTTP_200_OK,
			'data': order
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def update_order(db: Session, request: OrderUpdate, current_user : dict):
	try:
		user = get_user_or_404(db, current_user['user_id'])
		
		order = get_order_or_404(db, request.order_id)

		if order.status == 'draft':
			order.order_title = request.order_title or order.order_tile
			order.status = request.status or order.status
			order.updated_at = datetime.utcnow()
			order.updated_by = user.user_name

			db.commit()
			return {
				'mess' : 'Update order successfully !',
				'status_code' : status.HTTP_200_OK
			}
		else:
			raise HTTPException(
				detail= 'Order was submitted, cannot edit !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
	except Exception as ex:
		db.rollback()
		return get_internal_server_error(ex)

# High-level required: This allows admin and manager for approving or rejecting order which is submitted
async def change_status_of_order(db: Session, request: OrderApprove):
	try:
		order = get_order_or_404(db, request.order_id)
		order.status = request.status or order.status
		db.commit()
		db.refresh(order)
		return {
			'mess' : 'Change status of order successfully !',
			'status_code' : satus.HTTP_200_OK,
			'data' : order
		}

	except Exception as ex:
		db.rollback()
		return get_internal_server_error(ex)

# User required 
async def get_order_details_by_order(db: Session, order_id : int):
	try:
		od_details = db.query(OrderDetails).filter(OrderDetails.order_id == order_id).all()
		order_details = []
		for detail in od_details:
			product = get_product_or_404(db, detail.product_id)
			obj = {
				'product_id' : product.product_id,
				'product_name' : product.product_name,
				'sku_partnumber' : product.sku_partnumber,
				'description' : product.description,
				'price_for_customer' : detail.price_for_customer,
				'quantity' : detail.quantity,
				'service_contract_duration' : detail.service_contract_duration,
				'final_price' : detail.final_price
			}
			order_details.append(obj)
		return {
			'mess' : 'Get all order details of the order successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : order_details
		}
	except Exception as ex:
		return get_internal_server_error(ex)

# User required
async def delete_order(db: Session, order_id: int, current_user: dict):
	try:
		order = get_order_or_404(db, order_id)
		deal = get_deal_or_404(db, order.deal_id)

		if deal.user_id != current_user['user_id']:
			raise HTTPException(
				detail = 'Cannot remove order which is not your own !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		if order.status != 'draft':
			raise HTTPException(
				detail = 'The order is being processed ! Cannot remove !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		db.delete(order)
		db.commit()
		return {
			'mess' : 'Delete order successfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		db.rollback()
		return get_internal_server_error(ex)

# User required 
async def get_orders_by_deal(db: Session, deal_id: int):
	try:
		deal = get_deal_or_404(db, deal_id)
		return {
			'mess' : 'Get orders by deal succesfuly !',
			'status_code' : status.HTTP_200_OK,
			'data': db.query(Order).filter(Order.deal_id == deal_id).all()
		}
	except Exception as ex:
		return get_internal_server_error(ex)


async def get_orders_by_user(db: Session, current_user: dict):
	try:
		deals = db.query(Deal).filter(Deal.user_id == current_user['user_id']).all()
		ords = []
		for deal in deals:
			d = get_deal_or_404(db, deal.deal_id)
			obj = {
				'deal_id' : d.deal_id,
				'orders' : db.query(Order).filter(Order.deal_id == d.deal_id).all()
			}
			ords.append(obj)
		return {
			'mess' : 'Get orders by user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : ords
		}
	except Excecption as ex:
		return get_internal_server_error(ex)

# High-level required
async def get_orders(db: Session):
	try:
		orders = db.query(Order).filter(Order.status != 'draft').all()
		ods = []
		for order in orders:
			deal = get_deal_or_404(db, order.deal_id)
			obj = {
				'order_id' : order.order_id,
				'deal_id' : order.deal_id,
				'contact_name' : deal.contact_name,
				'contact_phone' : deal.contact_phone,
				'contact_email' : deal.contact_email,
				'address' : deal.address,
				'billing_address': deal.billing_address,
				'order_title': order.order_title,
				'total_budget' : order.total_budget,
				'status' : order.status
			}
			ods.append(obj)
		return {
			'mess' : 'Get all orders successfully !',
			'status_code': status.HTTP_200_OK,
			'data' : ods
		}
	except Exception as ex:
		return get_internal_server_error(ex)

# Admin required
async def get_orders_by_role(db: Session, role: str):
	try:
		deals = db.query(Deal).all()
		ods = []
		for deal in deals:
			user = get_user_or_404(db, deal.user_id)
			if user.role == role:
				orders = db.query(Order).filter(Order.deal_id == deal.deal_id).all()
				for order in orders:
					if order.status != 'draft':
						obj = {
							'order_id' : order.order_id,
							'order_title' : order.order_title,
							'customer_name': deal.customer_name,
							'user_email' : user.user_email,
							'created_at' : order.created_at,
							'total_budget' : order.total_budget,
							'status' : order.status
						}
						ods.append(obj)
		return {
			'mess' : 'Get orders by role successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : ods
		}

	except Exception as ex:
		return get_internal_server_error(ex)