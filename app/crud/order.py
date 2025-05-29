from sqlalchemy.orm import Session
from app.models import Order, OrderDetails, User, Product
from app.schemas import OrderCreate, OrderUpdate
from fastapi import Depends
from datetime import datetime
from fastapi import HTTPException, status

# User required
def create_order(db: Session, order : OrderCreate, current_user: dict):
	try:
		user = db.query(User).filter(User.user_id == current_user['user_id']).first()
		if user is None:
			raise HTTPException(
				detail= 'User not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)

		db_order = Order(
			user_id=user.user_id,
			order_title=order.order_title,
			created_by=user.user_name,
			customer_name=order.customer_name, 
			address = order.address,
			billing_address = order.address,
			status = order.status
		)
		db.add(db_order)
		db.commit()
		db.refresh(db_order)

		total_budget = 0

		for detail in order.details:
			final_price = 0
			product = db.query(Product).filter(Product.product_id == detail.product_id).first()

			if current_user['role'] == 'channels':
				final_price = product.channel_cost * detail.quantity
			else:
				if detail.price_for_customer < product.maximum_discount_price:
					raise HTTPException(
						detail= 'Price for customer cannot be lower than minimun price !',
						status_code = status.HTTP_400_BAD_REQUEST
					)
				final_price = detail.price_for_customer * detail.quantity

			# Increase the price through each year of contract duration
			for _ in range(detail.service_contract_duration - 1):
				final_price += 0.05 * final_price

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
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# Admin required
def get_orders(db: Session):
	try:
		# Here I'm getting all the orders, and about admin site, just get all orders that have status is not draft
		# Need to modify this code --> Because admin or manager just can see the orders which have the status if submitted
		orders = db.query(Order).all()
		ods = []
		for order in orders:
			user = db.query(User).filter(User.user_id == order.user_id).first()
			obj = {
				'order_id' : order.order_id,
				'order_title' : order.order_title,
				'customer_name' : order.customer_name,
				'user_name' : user.user_name,
				'user_email' : user.user_email,
				'phone' : user.phone,
				'company_name' : user.company_name,
				'total_budget' : order.total_budget,
				'status' : order.status,
				'address' : order.address,
				'billing_address' : order.billing_address
			}
			ods.append(obj)
		return {
			'mess' : 'Get orders by user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : ods
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# User required
def get_order(db: Session, order_id : int):
	try:
		order = db.query(Order).filter(Order.order_id == order_id).first()
		if order is None:
			raise HTTPException(
				detail= 'Order not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		return {
			'mess' : 'Get order successfully !',
			'status_code' : status.HTTP_200_OK,
			'data': order
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def get_order_by_user(db: Session, current_user: dict):
	try:
		user = db.query(User).filter(User.user_id == current_user['user_id']).first()
		if user is None:
			raise HTTPException(
				detail= 'User not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)

		orders = db.query(Order).filter(Order.user_id == user_id).all()
		ods = []
		for order in orders:
			user = db.query(User).filter(User.user_id == user_id).first()
			obj = {
				'order_id' : order.order_id,
				'order_title' : order.order_title,
				'user_email' : user.user_email,
				'company_name' : user.company_name,
				'total_budget' : order.total_budget,
				'status' : order.status,
				'address' : order.address,
				'billing_address' : order.billing_address
			}
			ods.append(obj)
		return {
			'mess' : 'Get orders by user successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : ods
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def update_order(db: Session, request: OrderUpdate, current_user : dict):
	try:
		user = db.query(User).filter(User.user_id == current_user['user_id']).first()
		if user is None:
			raise HTTPException(
				detail= 'User not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		
		order = db.query(Order).filter(Order.order_id == request.order_id).first()
		if order is None:
			raise HTTPException(
				detail= 'Order not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		if order.status == 'draft':
			order.order_title = request.order_title or order.order_tile
			order.customer_name = request.customer_name or order.customer_name
			order.status = request.status or order.status
			order.updated_at = datetime.utcnow()
			order.updated_by = user.user_name
			order.address = request.address or order.address
			order.billing_address = request.billing_address or order.billing_address

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
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# Admin required: This allows admin for approving or rejecting order which is submitted
def change_status_of_order(db: Session, admin: dict, status: str, order_id : int):
	try:
		order = db.query(Order).filter(Order.order_id == order_id).first()
		if order is None:
			raise HTTPException(
				detail= 'Order not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		order.status = status or order.status
		db.commit()
		db.refresh(order)
		return {
			'mess' : 'Change status of order successfully !',
			'status_code' : satus.HTTP_200_OK,
			'data' : order
		}

	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# User required 
def get_order_details_by_order(db: Session, order_id : int):
	try:
		od_details = db.query(OrderDetails).filter(OrderDetails.order_id == order_id).all()
		order_details = []
		for detail in od_details:
			product = db.query(Product).filter(Product.product_id == detail.product_id).first()
			if product is None:
				raise HTTPException(
					detail = 'Product not found !',
					status_code = status.HTTP_404_NOT_FOUND
				)
			obj = {
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
		raise HTTPException(
			detail = f'Somethign was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)