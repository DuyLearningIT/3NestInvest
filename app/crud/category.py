from sqlalchemy.orm import Session, load_only
from app.schemas import CreateCategory, UpdateCategory
from app.models import Category, Type
from datetime import datetime

def create_category(db: Session, request : CreateCategory):
	try:
		check = db.query(Category).filter(Category.category_name == request.category_name).first()
		if check:
			return {
				'mess' : 'Category has already existsed !',
				'status_code' : 400
			}
		check_type = db.query(Type).filter(Type.type_id == request.type_id).first()
		if check_type is None:
			return {
				'mess' : 'Cannot find the type !',
				'status_code' : 400
			}
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
			'status_code' : 201,
			'data': {
				'category_id' : new_cat.category_id,
				'category_name' : new_cat.category_name,
				'description' : new_cat.description,
				'created_at' : new_cat.created_at
			}
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}

def get_categories(db: Session):
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
			'status_code' : 200,
			'data' : categories
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}

def get_category(db: Session, category_id : int):
	try:
		cate = db.query(Category).filter(Category.category_id == category_id).first()
		if cate is None:
			return {
				'mess' : 'Category not found !',
				'status_code' : 404
			}
		type_ = db.query(Type).filter(Type.type_id == cate.type_id)
		return {
			'mess' : 'Get category successfully !',
			'status_code' : 200,
			'data' : {
				'category_id' : cate.category_id,
				'category_name' : cate.category_name,
				'description' : cate.description,
				'type_id' : cate.type_id,
				'type_name' : type_.type_name
			}
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}

def update_category(db: Session, request: UpdateCategory):
	try:
		cate = db.query(Category).filter(Category.category_id == request.category_id).first()
		if cate is None:
			return {
				'mess' : "Category not found !",
				'status_code' : 404
			}
		cate.category_name = request.category_name or cate.category_name
		cate.description = request.description or request.description
		cate.type_id = request.type_id or cate.type_id
		cate.updated_at = datetime.now()
		cate.updated_by = 'admin'
		db.commit()
		db.refresh(cate)
		return {
			'mess' : 'Update category successfully !',
			'status_code' : 200,
			'data' : {
				'category_name' : cate.category_name,
				'description' : cate.description,
				'type_id' : cate.type_id
			}
		}

	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}

def delete_category(db: Session, category_id):
	try:
		cate = db.query(Category).filter(Category.category_id == category_id).first()
		if cate is None:
			return {
				'mess' : "Category not found !",
				'status_code' : 404
			}
		db.delete(cate)
		db.commit()
		return {
			'mess' : 'Delete category successfully !',
			'status_code' : 204
		}
	except Exception as ex:
		return {
			'mess' : f'Something was wrong: {ex}',
			'status_code' : 500
		}
