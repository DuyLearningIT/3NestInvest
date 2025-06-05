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
			deal_id = order.deal_id,
			order_title=order.order_title,
			created_by=user.user_name,
			status = order.status,
		)
		db.add(db_order)
		db.commit()
		db.refresh(db_order)

		total_budget = 0
		initial_price = 0
		for detail in order.details:
			product = db.query(Product).filter(Product.product_id == detail.product_id).first()

			if product is None:
				raise HTTPException(
					detail= 'Product not found !',
					status_code = status.HTTP_404_NOT_FOUND
				)

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
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# Admin required: This allows admin and manager for approving or rejecting order which is submitted
def change_status_of_order(db: Session, status: str, order_id : int):
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

# User required
def delete_order(db: Session, order_id: int, current_user: dict):
	try:
		order = db.query(Order).filter(Order.order_id == order_id).first()
		if order is None:
			raise HTTPException(
				detail = 'Order not found !',
				status_code= status.HTTP_404_NOT_FOUND
			)
		deal = db.query(Deal).filter(Deal.deal_id == order.deal_id).first()
		if deal is None:
			raise HTTPException(
				detail = 'Deal not found !',
				status_code= status.HTTP_404_NOT_FOUND
			)
		if deal.user_id != current_user['user_id']:
			raise HTTPException(
				detail = 'Cannot remove order which is not your own !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		db.delete(order)
		db.commit()
		return {
			'mess' : 'Delete order successfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		raise HTTPException(
			detail = f'Something was wrong {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# User required 
async def get_orders_by_deal(db: Session, deal_id: int):
	try:
		deal = db.query(Deal).filter(Deal.deal_id == deal_id).first()
		if deal is None:
			raise HTTPException(
				detail = 'Deal not found !',
				status_code= status.HTTP_404_NOT_FOUND
			)
		return {
			'mess' : 'Get orders by deal succesfuly !',
			'status_code' : status.HTTP_200_OK,
			'data': db.query(Order).filter(Order.deal_id == deal_id).all()
		}
	except Exception as ex:
		raise HTTPException(
			detail = f'Something was wrong {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)