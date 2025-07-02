from sqlalchemy.orm import Session, load_only, joinedload
from app.schemas import CreateCategory, UpdateCategory
from app.models import Category, Type
from datetime import datetime
from fastapi import HTTPException, status, Request
from app.utils import get_internal_server_error, get_category_or_404, get_type_or_404, log_activity
from app.utils.permission_checking import check_permission

# Admin required
async def create_category(db: Session, request : CreateCategory, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'type', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		check = db.query(Category).filter(Category.category_name == request.category_name).first()
		if check:
			raise HTTPException(
				detail='Category has already existed !',
				status_code = status.HTTP_400_BAD_REQUEST
			)
		check_type = get_type_or_404(db, request.type_id)
		new_cat = Category(
			category_name = request.category_name,
			type_id = request.type_id,
			category_description = request.category_description
		)
		db.add(new_cat)
		db.commit()
		db.refresh(new_cat)
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Create category",
			target_type= "Category"
		)
		return {
			'mess' : 'Add category successfully !',
			'status_code' : status.HTTP_201_CREATED,
			'data': {
				'category_id' : new_cat.category_id,
				'category_name' : new_cat.category_name,
				'description' : new_cat.category_description,
				'created_at' : new_cat.created_at
			}
		}
	except Exception as ex:
		return get_internal_server_error(ex)

async def get_categories(db: Session, logRequest: Request, current_user: dict):
    try:
        results = (
            db.query(Category, Type)
            .join(Type, Category.type_id == Type.type_id)
            .all()
        )
        categories = []
        for cate, type_ in results:
            obj = {
                'category_id': cate.category_id,
                'category_name': cate.category_name,
                'description': cate.category_description,
                'type_name': type_.type_name
            }
            categories.append(obj)
        log_activity(
            db=db,
            request= logRequest,
            user_id= current_user['user_id'],
            activity_description= "Get all categories",
            target_type= "Category"
        )
        return {
            'mess': 'Get all categories successfully!',
            'status_code': status.HTTP_200_OK,
            'data': categories
        }
    except Exception as e:
        return {
            'mess': f'Error: {str(e)}',
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'data': []
        }

async def get_category(db: Session, category_id: int, logRequest: Request, current_user: dict):
    try:
        cate = db.query(Category).options(joinedload(Category.tb_type)).filter(Category.category_id == category_id).first()
        if not cate:
            raise HTTPException(status_code=404, detail="Category not found")
        
        log_activity(
            db=db,
            request=logRequest,
            user_id=current_user['user_id'],
            activity_description="Get a category",
            target_type="Category"
        )

        return {
            'mess': 'Get category successfully!',
            'status_code': status.HTTP_200_OK,
            'data': {
                'category_id': cate.category_id,
                'category_name': cate.category_name,
                'description': cate.category_description,
                'type_id': cate.type_id,
                'type_name': cate.tb_type.type_name if cate.tb_type else None
            }
        }
    except Exception as ex:
        return get_internal_server_error(ex)


async def update_category(db: Session, request: UpdateCategory, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'type', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		cate = get_category_or_404(db, request.category_id)
		cate.category_name = request.category_name or cate.category_name
		cate.category_description = request.category_description or request.category_description
		cate.type_id = request.type_id or cate.type_id
		cate.updated_at = datetime.now()
		cate.updated_by = current_user['user_name']
		db.commit()
		db.refresh(cate)
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Update a category",
			target_type= "Category"
		)
		return {
			'mess' : 'Update category successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : {
				'category_name' : cate.category_name,
				'category_description' : cate.category_description,
				'type_id' : cate.type_id
			}
		}

	except Exception as ex:
		return get_internal_server_error(ex)

async def delete_category(db: Session, category_id: int, logRequest: Request, current_user: dict):
	try:
		permission = await check_permission(db, 'manage', 'type', current_user['role_id'])
		if not permission:
			return {
				'mess' : "You don't have permission for accessing this function !",
				'status_code' : status.HTTP_403_FORBIDDEN 
			}
		cate = get_category_or_404(db, category_id)
		db.delete(cate)
		db.commit()
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Delete a category",
			target_type= "Category"
		)
		return {
			'mess' : 'Delete category successfully !',
			'status_code' : status.HTTP_204_NO_CONTENT
		}
	except Exception as ex:
		raise HTTPException(
			detail=f'Something was wrong: {ex}',
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		)
 
async def get_categories_by_type(db: Session, type_id: int, logRequest: Request, current_user: dict):
	try:
		# permission = await check_permission(db, 'manage', 'type', current_user['role_id'])
		# if not permission:
		# 	return {
		# 		'mess' : "You don't have permission for accessing this function !",
		# 		'status_code' : status.HTTP_403_FORBIDDEN 
		# 	}
		log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Get all categories by type",
			target_type= "Category"
		)
		return{
			'mess' : 'Get categories by type successfully !',
			'status_code' : status.HTTP_200_OK,
			'data' : db.query(Category).filter(Category.type_id == type_id).all()
		}
	except Exception as ex:
		return get_internal_server_error(ex)