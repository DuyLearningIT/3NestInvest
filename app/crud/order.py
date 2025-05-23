from sqlalchemy.orm import Session
from app.models import Order, OrderDetails, User, Product
from app.schemas import OrderCreate, OrderUpdate
from fastapi import Depends
from datetime import datetime

def create_order(db: Session, order : OrderCreate, current_user: dict):
    try:
        user = db.query(User).filter(User.user_id == current_user['user_id']).first()
        if user is None:
            return {'mess': 'User not found!', 'status_code': 404}

        db_order = Order(
            user_id=user.user_id,
            order_title=order.order_title,
            created_by=user.user_name,
            customer_name=order.customer_name
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        total_budget = 0

        for detail in order.details:
            product = db.query(Product).filter(Product.product_id == detail.product_id).first()

            if detail.discount_percent > product.maximum_discount:
                return {
                    'mess': 'Discount percent cannot exceed maximum!',
                    'status_code': 400
                }

            final_price = product.price * detail.quantity * (1 - (detail.discount_percent / 100))
            total_budget += final_price

            db_detail = OrderDetails(
                order_id=db_order.order_id,
                product_id=detail.product_id,
                quantity=detail.quantity,
                discount_percent=detail.discount_percent,
                final_price=final_price
            )
            db.add(db_detail)

        db_order.total_budget = total_budget
        db.commit()

        return {
            'mess': 'Create order successfully!',
            'status_code': 201,
            'data': db_order
        }

    except Exception as ex:
        return {
            'mess': f'Something was wrong: {ex} !',
            'status_code': 500
        }

def get_orders(db: Session):
	try:
		orders = db.query(Order).filter(Order.status != 'draft').all()
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
				'status' : order.status
			}
			ods.append(obj)
		return {
			'mess' : 'Get orders by user successfully !',
			'status_code' : 200,
			'data' : ods
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}

def get_order(db: Session, order_id : int):
	try:
		order = db.query(Order).filter(Order.order_id == order_id).first()
		if order is None:
			return {
				'mess' : 'Order not found !',
				'status_code' : 404
			}
		return {
			'mess' : 'Get order successfully !',
			'status_code' : 200,
			'data': order
		}
	except Exception as ex:
		return {
			'mess': f'Something was wrong: {ex}',
			'status_code' : 500
		}

def get_order_by_user(db: Session, current_user: dict):
	try:
		user = db.query(User).filter(User.user_id == current_user['user_id']).first()
		if user is None:
			return {'mess': 'User not found!', 'status_code': 404}

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
				'status' : order.status
			}
			ods.append(obj)
		return {
			'mess' : 'Get orders by user successfully !',
			'status_code' : 200,
			'data' : ods
		}
	except Exception as ex:
		return {
			'mess': f'Something was wrong: {ex}',
			'status_code' : 500
		}

def update_order(db: Session, request: OrderUpdate, current_user : dict):
	try:
		user = db.query(User).filter(User.user_id == current_user['user_id']).first()
		if user is None:
			return {'mess': 'User not found!', 'status_code': 404}
		
		order = db.query(Order).filter(Order.order_id == request.order_id).first()
		if order is None:
			return {
				'mess' : 'Order not found !',
				'status_code' : 404
			}
		if order.status == 'draft':
			order.order_title = request.order_title or order.order_tile
			order.customer_name = request.customer_name or order.customer_name
			order.status = request.status or order.status
			order.updated_at = datetime.utcnow()
			order.updated_by = user.user_name

			db.commit()
			return {
				'mess' : 'Update order successfully !',
				'status_code' : 200
			}
		else:
			return{
				'mess' : 'Order was submitted, you cannot edit !',
				'status_code' : 400
			}
	except Exception as ex:
		return {
			'mess': f'Something was wrong: {ex}',
			'status_code' : 500
		}
