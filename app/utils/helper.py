from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User, Deal, Category, Type, Order, UserRequest, Product, PermissionType, Permission

def get_internal_server_error(ex):
	raise HTTPException(
		detail = f'Something was wrong: {ex}',
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
	)

def get_user_or_404(db: Session, user_id : int) -> User:
	user = db.query(User).filter(User.user_id == user_id).first()
	if not user:
		raise HTTPException(
			detail = 'User not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
	return user

def get_deal_or_404(db: Session, deal_id : int ) -> Deal:
	deal = db.query(Deal).filter(Deal.deal_id == deal_id).first()
	if not deal:
		raise HTTPException(
			detail = 'Deal not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
	return deal

def get_category_or_404(db: Session, category_id : int) -> Category:
	category = db.query(Category).filter(Category.category_id == category_id).first()
	if not category:
		raise HTTPException(
			detail = 'Category not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
	return category 

def get_type_or_404(db: Session, type_id : int) -> Type:
	type_ = db.query(Type).filter(Type.type_id == type_id).first()
	if not type_:
		raise HTTPException(
			detail = 'Type not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
	return type_

def get_product_or_404(db: Session, product_id) -> Product:
	product = db.query(Product).filter(Product.product_id == product_id).first()
	if not product:
		raise HTTPException(
			detail = 'Product not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
	return product

def get_order_or_404(db: Session, order_id: int) -> Order:
	order = db.query(Order).filter(Order.order_id == order_id).first()
	if not order:
		raise HTTPException(
			detail = 'Order not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
	return order 

def get_request_or_404(db: Session, request_id : int) -> UserRequest:
	request = db.query(UserRequest).filter(UserRequest.request_id == request_id).first()
	if not request:
		raise HTTPException(
			detail = 'Request not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
	return request

def get_permission_type_or_404(db: Session, request_id : int) -> PermissionType:
	permission_type = db.query(PermissionType).filter(PermissionType.permission_type_id == request_id).first()
	if not permission_type:
		raise HTTPException(
			detail = 'PermissionType not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
	return permission_type

def get_permission_or_404(db: Session, request_id: int) -> Permission:
	permission = db.query(Permission).filter(Permission.permission_id == request_id).first()
	if not permission:
		raise HTTPException(
			detail = 'Permission not found !',
			status_code = status.HTTP_404_NOT_FOUND
		)
	return permission