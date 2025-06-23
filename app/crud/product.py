from sqlalchemy.orm import Session, load_only, joinedload
from app.models import Product, Category, Type
from app.schemas import CreateProduct, UpdateProduct
from datetime import datetime
from fastapi import HTTPException, status, Request
from app.utils import get_internal_server_error, get_type_or_404, get_category_or_404, log_activity, get_product_or_404
from app.utils.permission_checking import check_permission

# Admin required
async def create_product(db: Session, request : CreateProduct, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'product', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		pro = db.query(Product).filter(Product.product_name == request.product_name).first()
		if pro:
			raise HTTPException(
				detail= 'Product has already existed !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		cate = get_category_or_404(db, request.category_id)
		new_pro = Product(
			product_name = request.product_name,
			product_description = request.product_description,
			sku_partnumber = request.sku_partnumber,
			price = request.price,
			maximum_discount = request.maximum_discount,
			category_id = request.category_id,
			product_role = request.product_role,
			channel_cost = request.channel_cost,
			created_by = current_user['user_name']
		)
		db.add(new_pro)
		db.commit()
		db.refresh(new_pro)
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Create product",
			target_type= "Product"
		)
		return {
			'mess' : 'Create product successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data' : {
				'product_id' : new_pro.product_id,
				'product_name' : new_pro.product_name,
				'sku_partnumber' : new_pro.sku_partnumber,
				'description' : new_pro.product_description,
				'price' : new_pro.price,
				'product_role' : new_pro.product_role,
				'category_name': db.query(Category).options(load_only(Category.category_name)).filter(Category.category_id == new_pro.category_id).first(),
				'maximum_discount' : new_pro.maximum_discount,
				'maximum_discount_price' : new_pro.maximum_discount_price ,
				'channel_cost' : new_pro.channel_cost,
				'created_at' : new_pro.created_at,
				'created_by' : new_pro.created_by
			}
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_products(db: Session, logRequest: Request, current_user: dict):
	try:
		products_query = db.query(Product) \
			.options(joinedload(Product.category).joinedload(Category.tb_type)) \
			.all()

		products = []
		for pro in products_query:
			if pro.status == 'inactive':
				continue

			cate = pro.category
			type_ = cate.tb_type if cate else None

			products.append({
				'product_id': pro.product_id,
				'product_name': pro.product_name,
				'sku_partnumber': pro.sku_partnumber,
				'product_role': pro.product_role,
				'description': pro.product_description,
				'price': pro.price,
				'category_name': cate.category_name if cate else None,
				'type_name': type_.type_name if type_ else None,
				'maximum_discount': pro.maximum_discount,
				'maximum_discount_price': pro.maximum_discount_price,
				'channel_cost': pro.channel_cost,
				'created_at': pro.created_at,
				'status': pro.status
			})

		log_activity(
			db=db,
			request=logRequest,
			user_id=current_user['user_id'],
			activity_description="Get all products",
			target_type="Product"
		)

		return {
			'mess': 'Get all products successfully!',
			'status_code': status.HTTP_200_OK,
			'data': products
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_product(db: Session, product_id : int, logRequest: Request, current_user: dict):
	try:
		pro = get_product_or_404(db, product_id)
		cate = get_category_or_404(db, pro.category_id)
		type_ = get_type_or_404(db, cate.type_id)
		log_activity(
				db=db,
				request= logRequest,
				user_id= current_user['user_id'],
				activity_description= "Get product by id",
				target_type= "Product"
		)
		return {
			'mess' : 'Get product successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data' : {
				'product_id' : pro.product_id,
				'product_name' : pro.product_name,
				'sku_partnumber' : pro.sku_partnumber,
				'product_role' : pro.product_role,
				'description' : pro.product_description,
				'price' : pro.price,
				'category_name': cate.category_name,
				'type_name' : type_.type_name,
				'maximum_discount' : pro.maximum_discount,
				'maximum_discount_price' : pro.maximum_discount_price,
				'channel_cost' : pro.channel_cost,
				'created_at' : pro.created_at,
				'status' : pro.status
			}
		}
	except Exception as ex:
		return get_internal_server_error(ex)
	
# Admin required
async def update_product(db: Session, request : UpdateProduct, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'product', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		permission = await check_permission(db, 'manage', 'user', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		pro = get_product_or_404(db, request.product_id)
		pro.product_name = request.product_name or pro.product_name
		pro.category_id = request.category_id or pro.category_id
		pro.product_description = request.product_description or pro.product_description
		pro.sku_partnumber = request.sku_partnumber or pro.sku_partnumber
		pro.price = request.price or pro.price
		pro.maximum_discount = request.maximum_discount or pro.maximum_discount
		pro.maximum_discount_price = pro.price - ( pro.maximum_discount * pro.price ) / 100
		pro.channel_cost  = request.channel_cost or pro.channel_cost
		pro.status = request.status or pro.status
		pro.updated_at = datetime.utcnow()
		pro.updated_by = current_user['user_name']

		db.commit()
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Update product",
			target_type= "Product"
		)
		return {
			'mess' : 'Update product successfully !',
			'status_code' : status.HTTP_200_OK
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_products_by_category(db: Session, category_id: int, logRequest: Request, current_user: dict):
	try:
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Get all products by category",
			target_type= "Product"
		)
		return {
			'mess' : 'Get products by category successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : db.query(Product).options(load_only(
					Product.product_id, 
					Product.product_name, 
					Product.product_description,
					Product.category_id, 
					Product.price, 
					Product.sku_partnumber, 
					Product.maximum_discount,
					Product.maximum_discount_price,
					Product.channel_cost
				)).filter(Product.category_id == category_id, Product.status =='active').all()
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_products_by_type(db: Session, type_id: int, logRequest: Request, current_user: dict):
	try:
		type_ = get_type_or_404(db, type_id)

		categories = db.query(Category) \
			.options(joinedload(Category.products)) \
			.filter(Category.type_id == type_id).all()

		pros = []
		for cate in categories:
			for pro in cate.products:
				if pro.status == 'inactive':
					continue
				pros.append({
					'product': pro,
					'category_name': cate.category_name
				})

		log_activity(
			db=db,
			request=logRequest,
			user_id=current_user['user_id'],
			activity_description="Get all products by type",
			target_type="Product"
		)

		return {
			'mess': 'Get all products by type successfully!',
			'status_code': status.HTTP_200_OK,
			'data': pros
		}

	except Exception as ex:
		return get_internal_server_error(ex)

async def delete_product(db: Session, product_id : int, logRequest: Request, current_user : dict):
	try:
		permission = await check_permission(db, 'manage', 'product', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		pro = get_product_or_404(db, product_id)
		db.delete(pro)
		db.commit()
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Delete product",
			target_type= "Product"
		)
		return {
			'mess' : 'Delete product succesfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		return get_internal_server_error(ex)

# User required
async def get_products_by_role(db: Session, logRequest: Request, current_user: dict):
	try:
		products_query = db.query(Product).options(
			joinedload(Product.category).joinedload(Category.tb_type)
		).filter(Product.product_role == current_user['role_id'])

		products = []
		for pro in products_query:
			cate = pro.category
			type_ = cate.tb_type if cate else None

			obj = {
				'product_id': pro.product_id,
				'product_name': pro.product_name,
				'sku_partnumber': pro.sku_partnumber,
				'product_role': pro.product_role,
				'description': pro.product_description,
				'price': pro.price,
				'category_name': cate.category_name if cate else None,
				'maximum_discount': pro.maximum_discount,
				'maximum_discount_price': pro.maximum_discount_price,
				'channel_cost': pro.channel_cost,
				'created_at': pro.created_at,
				'status': pro.status
			}
			products.append(obj)

		log_activity(
			db=db,
			request=logRequest,
			user_id=current_user['user_id'],
			activity_description="Get all products by role",
			target_type="Product"
		)

		return {
			'mess': 'Get all products successfully!',
			'status_code': status.HTTP_200_OK,
			'data': products
		}

	except Exception as ex:
		return get_internal_server_error(ex)

# Admin required
async def get_products_by_role_and_type(db: Session, role_id: int, type_id: int, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'product', current_user['role_id'])
		if not permission:
			return {
				'mess': "You don't have permission for accessing this function!",
				'status_code': status.HTTP_403_FORBIDDEN
			}

		products_query = db.query(Product).options(
			joinedload(Product.category).joinedload(Category.tb_type)
		).filter(
			Product.product_role == role_id,
			Product.status != 'inactive'
		)

		pros = []
		for pro in products_query:
			cate = pro.category
			if not cate or cate.type_id != type_id:
				continue

			obj = {
				'product_id': pro.product_id,
				'product_name': pro.product_name,
				'sku_partnumber': pro.sku_partnumber,
				'product_role': pro.product_role,
				'description': pro.product_description,
				'price': pro.price,
				'category_name': cate.category_name if cate else None,
				'maximum_discount': pro.maximum_discount,
				'maximum_discount_price': pro.maximum_discount_price,
				'channel_cost': pro.channel_cost,
				'created_at': pro.created_at,
				'status': pro.status
			}
			pros.append(obj)

		log_activity(
			db=db,
			request=logRequest,
			user_id=current_user['user_id'],
			activity_description="Get all products by role and type",
			target_type="Product"
		)

		return {
			'mess': 'Get products successfully!',
			'status_code': status.HTTP_200_OK,
			'data': pros
		}
	except Exception as ex:
		return get_internal_server_error(ex)

# User required
# This function is used for user who log-in into our website and with their role
async def get_products_by_category_and_role(db: Session, category_id: int, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'product', current_user['role_id'])
		if not permission:
			return {
				'mess': "You don't have permission for accessing this function!",
				'status_code': status.HTTP_403_FORBIDDEN
			}

		products = db.query(Product).options(
			joinedload(Product.category)
		).filter(
			Product.product_role == current_user['role_id'],
			Product.category_id == category_id,
			Product.status != 'inactive'
		).all()

		cate = get_category_or_404(db, category_id)

		pros = []
		for pro in products:
			obj = {
				'product_id': pro.product_id,
				'product_name': pro.product_name,
				'sku_partnumber': pro.sku_partnumber,
				'product_role': pro.product_role,
				'description': pro.product_description,
				'price': pro.price,
				'category_name': cate.category_name,
				'maximum_discount': pro.maximum_discount,
				'maximum_discount_price': pro.maximum_discount_price,
				'channel_cost': pro.channel_cost,
				'created_at': pro.created_at,
				'status': pro.status
			}
			pros.append(obj)

		log_activity(
			db=db,
			request=logRequest,
			user_id=current_user['user_id'],
			activity_description="Get all products by category and role",
			target_type="Product"
		)

		return {
			'mess': 'Get products by role and category successfully!',
			'status_code': status.HTTP_200_OK,
			'data': pros
		}
	except Exception as ex:
		return get_internal_server_error(ex)