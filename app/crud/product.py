from sqlalchemy.orm import Session, load_only, joinedload
from app.models import Product, Category, Type
from app.schemas import CreateProduct, UpdateProduct
from datetime import datetime
from fastapi import HTTPException, status

# Admin required
def create_product(db: Session, request : CreateProduct, admin: dict):
	try:
		pro = db.query(Product).filter(Product.product_name == request.product_name).first()
		if pro:
			raise HTTPException(
				detail= 'Product has already existed !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		cate = db.query(Category).filter(Category.category_id == request.category_id).first()
		if cate is None:
			raise HTTPException(
				detail= 'Category not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		new_pro = Product(
			product_name = request.product_name,
			description = request.description,
			sku_partnumber = request.sku_partnumber,
			price = request.price,
			maximum_discount = request.maximum_discount,
			category_id = request.category_id,
			product_role = request.product_role,
			created_by = admin['user_name']
		)
		db.add(new_pro)
		db.commit()
		db.refresh(new_pro)
		return {
			'mess' : 'Create product successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data' : {
				'product_id' : new_pro.product_id,
				'product_name' : new_pro.product_name,
				'sku_partnumber' : new_pro.sku_partnumber,
				'desciption' : new_pro.description,
				'price' : new_pro.price,
				'product_role' : new_pro.product_role,
				'category_name': db.query(Category).options(load_only(Category.category_name)).filter(Category.category_id == new_pro.category_id).first(),
				'maximum_discount' : new_pro.maximum_discount,
				'maximum_discount_price' : new_pro.maximum_discount_price ,
				'created_at' : new_pro.created_at,
				'created_by' : new_pro.created_by
			}
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def get_products(db : Session):
	try:
		pros = db.query(Product).all()
		products = []
		for pro in pros:
			cate = db.query(Category).filter(Category.category_id == pro.category_id).first()
			type_ = db.query(Type).filter(Type.type_id == cate.type_id).first()
			obj = {
				'product_id' : pro.product_id,
				'product_name' : pro.product_name,
				'sku_partnumber' : pro.sku_partnumber,
				'product_role' : pro.product_role,
				'desciption' : pro.description,
				'price' : pro.price,
				'category_name': cate.category_name,
				'type_name' : type_.type_name,
				'maximum_discount' : pro.maximum_discount,
				'maximum_discount_price' : pro.maximum_discount_price ,
				'created_at' : pro.created_at,
				'status' : pro.status
			}
			products.append(obj)
		return {
			'mess' : 'Get all products successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : products
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def get_product(db: Session, product_id : int):
	try:
		pro = db.query(Product).filter(Product.product_id == product_id).first()
		if pro is None:
			raise HTTPException(
				detail= 'product not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		cate = db.query(Category).filter(Category.category_id == pro.category_id).first()
		if cate is None:
			raise HTTPException(
				detail= 'Category not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		type_ = db.query(Type).filter(Type.type_id == cate.type_id).first()
		if type_ is None:
			raise HTTPException(
				detail= 'Type not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		return {
			'mess' : 'Get product successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data' : {
				'product_id' : pro.product_id,
				'product_name' : pro.product_name,
				'sku_partnumber' : pro.sku_partnumber,
				'product_role' : pro.product_role,
				'desciption' : pro.description,
				'price' : pro.price,
				'category_name': cate.category_name,
				'type_name' : type_.type_name,
				'maximum_discount' : pro.maximum_discount,
				'maximum_discount_price' : pro.maximum_discount_price ,
				'created_at' : pro.created_at,
				'status' : pro.status
			}
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)
	
# Admin required
def update_product(db: Session, request : UpdateProduct, admin: dict):
	try:
		pro = db.query(Product).filter(Product.product_id == request.product_id).first()
		if pro is None:
			raise HTTPException(
				detail= 'Product not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		pro.product_name = request.product_name or pro.product_name
		pro.category_id = request.category_id or pro.category_id
		pro.description = request.description or pro.description
		pro.sku_partnumber = request.sku_partnumber or pro.sku_partnumber
		pro.price = request.price or pro.price
		pro.maximum_discount = request.maximum_discount or pro.maximum_discount
		pro.maximum_discount_price = pro.price - ( pro.maximum_discount * pro.price ) / 100
		pro.status = request.status or pro.status
		pro.updated_at = datetime.utcnow()
		pro.updated_by = admin['user_name']

		db.commit()
		return {
			'mess' : 'Update product successfully !',
			'status_code' : status.HTTP_200_OK
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def get_products_by_category(db: Session, category_id: int):
	try:
		return {
			'mess' : 'Get products by category successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : db.query(Product).options(load_only(
					Product.product_id, 
					Product.product_name, 
					Product.description,
					Product.category_id, 
					Product.price, 
					Product.sku_partnumber, 
					Product.maximum_discount,
					Product.maximum_discount_price 
				)).filter(Product.category_id == category_id).all()
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

def get_products_by_type(db: Session, type_id: int):
	try:
		# Check if needed, then -> Add
		# type_ = db.query(Type).filter(Type.type_id == type_id).first()
		# if type_ is None:
		# 	return {
		# 		'mess' : 'Type not found !',
		# 		'status_code': 404
		# 	}
		cates = db.query(Category).filter(Category.type_id == type_id).all()
		pros = []
		for cate in cates:
			products = db.query(Product).filter(Product.category_id == cate.category_id).all()
			for pro in products:
				obj = {
					'product' : pro,
					'category_name': cate.category_name
				}
				pros.append(obj)
		return {
			'mess' : 'Get all products by type successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : pros
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# Admin required
def delete_product(db: Session, product_id : int):
	try:
		pro = db.query(Product).filter(Product.product_id == product_id).first()
		if pro is None:
			raise HTTPException(
				detail= 'Product not found !',
				status_code = status.HTTP_404_NOT_FOUND
			)
		db.delete(pro)
		db.commit()
		return {
			'mess' : 'Delete product succesfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)
# Admin require
def get_products_by_role(db: Session, role: str):
	try:
		pros = db.query(Product).filter(Product.product_role == role).all()
		products = []
		for pro in pros:
			cate = db.query(Category).filter(Category.category_id == pro.category_id).first()
			type_ = db.query(Type).filter(Type.type_id == cate.type_id).first()
			obj = {
				'product_id' : pro.product_id,
				'product_name' : pro.product_name,
				'sku_partnumber' : pro.sku_partnumber,
				'product_role' : pro.product_role,
				'desciption' : pro.description,
				'price' : pro.price,
				'category_name': cate.category_name,
				'maximum_discount' : pro.maximum_discount,
				'maximum_discount_price' : pro.maximum_discount_price ,
				'created_at' : pro.created_at,
				'status' : pro.status
			}
			products.append(obj)
		return {
			'mess' : 'Get all products successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : products
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)

# Admin required
def get_products_by_role_and_type(db: Session, role: str, type_id: int):
	try:
		products = db.query(Product).filter(Product.product_role == role).all()
		pros = []
		for pro in products:
			cate = db.query(Category).filter(Category.category_id == pro.category_id).first()
			# Can determine whether category is None or not
			if cate.type_id == type_id:
				obj = {
					'product_id' : pro.product_id,
					'product_name' : pro.product_name,
					'sku_partnumber' : pro.sku_partnumber,
					'product_role' : pro.product_role,
					'description' : pro.description,
					'price' : pro.price,
					'category_name': cate.category_name,
					'maximum_discount' : pro.maximum_discount,
					'maximum_discount_price' : pro.maximum_discount_price ,
					'created_at' : pro.created_at,
					'status' : pro.status
				}
				pros.append(obj)
		return {
			'mess': 'Get products successflly !',
			'status_code' : status.HTTP_200_OK,
			'data': pros
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)