from sqlalchemy.orm import Session, load_only
from app.schemas import CreateCategory, UpdateCategory
from app.models import Category, Type
from datetime import datetime
from fastapi import HTTPException, status
from app.utils import get_internal_server_error, get_category_or_404, get_type_or_404

# Admin required
async def create_category(db: Session, request : CreateCategory, admin: dict):
	try:
		check = db.query(Category).filter(Category.category_name == request.category_name).first()
		if check:
			raise HTTPException(
				detail='Category has already existed !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		check_type = get_type_or_404(db. request.type_id)
		new_cat = Category(
			category_name = request.category_name,
			type_id = request.type_id,
			description = request.description
		)
		db.add(new_cat)
		db.commit()
		db.refresh(new_cat)
		return {
			'mess' : 'Add category successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data': {
				'category_id' : new_cat.category_id,
				'category_name' : new_cat.category_name,
				'description' : new_cat.description,
				'created_at' : new_cat.created_at
			}
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_categories(db: Session):
	try:
		cates = db.query(Category).all()
		categories = []
		for cate in cates:
			type_ = db.query(Type).filter(Type.type_id == cate.type_id).first()
			obj = {
				'category_id' : cate.category_id,
				'category_name' : cate.category_name,
				'description' : cate.description,
				'type_name' : type_.type_name
			}
			categories.append(obj)

		return {
			'mess' : 'Get all categories successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : categories
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_category(db: Session, category_id : int):
	try:
		cate = get_category_or_404(db, category_id)
		type_ = db.query(Type).filter(Type.type_id == cate.type_id)
		return {
			'mess' : 'Get category successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : {
				'category_id' : cate.category_id,
				'category_name' : cate.category_name,
				'description' : cate.description,
				'type_id' : cate.type_id,
				'type_name' : type_.type_name
			}
		}
	except Exception as ex:
		return get_internal_server_error(ex)

# Admin required
async def update_category(db: Session, request: UpdateCategory, admin: dict):
	try:
		cate = get_category_or_404(db, request.category_id)
		cate.category_name = request.category_name or cate.category_name
		cate.description = request.description or request.description
		cate.type_id = request.type_id or cate.type_id
		cate.updated_at = datetime.now()
		cate.updated_by = 'admin'
		db.commit()
		db.refresh(cate)
		return {
			'mess' : 'Update category successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : {
				'category_name' : cate.category_name,
				'description' : cate.description,
				'type_id' : cate.type_id
			}
		}

	except Exception as ex:
		return get_internal_server_error(ex)

# Admin required
async def delete_category(db: Session, category_id: int, admin: dict):
	try:
		cate = get_category_or_404(db, category_id)
		db.delete(cate)
		db.commit()
		return {
			'mess' : 'Delete category successfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)
 
async def get_categories_by_type(db: Session, type_id: int):
	try:
		return{
			'mess' : 'Get categories by type successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : db.query(Category).filter(Category.type_id == type_id).all()
		}
	except Exception as ex:
		return get_internal_server_error(ex)