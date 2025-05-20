from sqlalchemy.orm import Session, load_only
from app.models import Product, Category
from app.schemas import CreateProduct, UpdateProduct
from datetime import datetime

def create_product(db: Session, request : CreateProduct):
	try:
		pro = db.query(Product).filter(Product.product_name == request.product_name).first()
		if pro:
			return {
				'mess' : 'Product has already existsed !',
				'status_code' : 400
			}
		cate = db.query(Category).filter(Category.category_id == request.category_id).first()
		if cate is None:
			return {
				'mess' : 'Cannot find Category !',
				'status_code' : 404
			}
		new_pro = Product(
			product_name = request.product_name,
			description = request.description,
			sku_partnumber = request.sku_partnumber,
			price = request.price,
			maximum_discount = request.maximum_discount,
			category_id = request.category_id
		)
		db.add(new_pro)
		db.commit()
		db.refresh(new_pro)
		return {
			'mess' : 'Create product successfully !',
			'status_code' : 201,
			'data' : {
				'product_id' : new_pro.product_id,
				'product_name' : new_pro.product_name,
				'sku_partnumber' : new_pro.sku_partnumber,
				'desciption' : new_pro.description,
				'price' : new_pro.price,
				'category_id' : new_pro.category_id,
				'maximum_discount' : new_pro.maximum_discount,
				'maximum_discoutn_price' : new_pro.maximum_discount_price ,
				'created_at' : new_pro.created_at
			} 
		}
	except Exception as ex:
		return {
			'mess': f'Something was wrong: {ex}',
			'status_code' : 500
		}

def get_products(db : Session):
	try:
		return {
			'mess' : 'Get all products successfully !',
			'status_code' : 200,
			'data' : db.query(Product).options(load_only(
					Product.product_id, 
					Product.product_name, 
					Product.description,
					Product.category_id, 
					Product.price, 
					Product.sku_partnumber, 
					Product.maximum_discount,
					Product.maximum_discount_price 
				)).all()
		}
	except Exception as ex:
		return {
			'mess': f'Something was wrong: {ex}',
			'status_code' : 500
		}

def get_product(db: Session, product_id : int):
	try:
		pro = db.query(Product).options(load_only(
					Product.product_id,
					Product.product_name,
					Product.description,
					Product.category_id, 
					Product.price, 
					Product.sku_partnumber, 
					Product.maximum_discount,
					Product.maximum_discount_price
				)).filter(Product.product_id == product_id).first()
		if pro is None:
			return {
				'mess' : 'Product not found !',
				'status_code': 404
			}
		return {
			'mess' : 'Get product successfully !',
			'status_code' : 200,
			'data' : pro
		}
	except Exception as ex:
		return {
			'mess': f'Something was wrong: {ex}',
			'status_code' : 500
		}

def update_product(db: Session, request : UpdateProduct):
	try:
		pro = db.query(Product).filter(Product.product_id == request.product_id).first()
		if pro is None:
			return {
				'mess' : 'Product not found !',
				'status_code' : 404
			}
		pro.product_name = request.product_name or pro.product_name
		pro.category_id = request.category_id or pro.category_id
		pro.description = request.description or pro.description
		pro.sku_partnumber = request.sku_partnumber or pro.sku_partnumber
		pro.price = request.price or pro.price
		pro.maximum_discount = request.maximum_discount or pro.maximum_discount
		pro.maximum_discount_price = pro.price - ( pro.maximum_discount * pro.price ) / 100
		pro.status = request.status or pro.status
		pro.updated_at = datetime.utcnow()
		pro.updated_by = 'admin'

		db.commit()
		return {
			'mess' : 'Update product successfully !',
			'status_code' : 200,
			'data' : {
				'product_id' : pro.product_id,
				'product_name' : pro.product_name,
				'sku_partnumber' : pro.sku_partnumber,
				'desciption' : pro.description,
				'price' : pro.price,
				'category_id' : pro.category_id,
				'maximum_discount' : pro.maximum_discount,
				'maximum_discoutn_price' : pro.maximum_discount_price ,
				'updated_at' : pro.updated_at
			}
		}
	except Exception as ex:
		return {
			'mess': f'Something was wrong: {ex}',
			'status_code' : 500
		}

def get_products_by_category(db: Session, category_id: int):
	try:
		return {
			'mess' : 'Get products by category successfully !',
			'status_code' : 200,
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
		return {
			'mess': f'Something was wrong: {ex}',
			'status_code' : 500
		}

def get_products_by_type(db: Session, type_id: int):
	try:
		return {
			'mess' : 'Get products by category successfully !',
			'status_code' : 200,
			'data' : db.query(Product).join(Category).options(load_only(
					Product.product_id, 
					Product.product_name, 
					Product.description,
					Product.category_id, 
					Product.price, 
					Product.sku_partnumber, 
					Product.maximum_discount,
					Product.maximum_discount_price 
				)).filter(Category.type_id == type_id).all()
		}
	except Exception as ex:
		return {
			'mess': f'Something was wrong: {ex}',
			'status_code' : 500
		}

def delete_product(db: Session, product_id : int):
	try:
		pro = db.query(Product).filter(Product.product_id == product_id).first()
		if pro is None:
			return {
				'mess' : 'product not found !',
				'status_code' : 404
			}
		db.delete(pro)
		db.commit()
		return {
			'mess' : 'Delete product succesfully !',
			'status_code' : 204
		}
	except Exception as ex:
		return {
			'mess': f'Something was wrong: {ex}',
			'status_code' : 500
		}
