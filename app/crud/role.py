from sqlalchemy.orm import Session, joinedload
from app.models import Permission, Role, RolePermission
from app.schemas import RoleCreate, RoleUpdate
from datetime import datetime
from fastapi import HTTPException, status, Request
from app.utils import get_internal_server_error, log_activity
from app.utils.permission_checking import check_permission


async def create_role(db: Session, request: RoleCreate, logRequest: Request, current_user: dict):
    try:
        permission = await check_permission(db, 'manage', 'role', current_user['role_id'])
        if not permission:
            return {
                'mess' : "You don't have permission for accessing this function !",
                'status_code' : status.HTTP_403_FORBIDDEN 
        }
        existing_role = db.query(Role).filter(Role.role_name == request.role_name).first()
        if existing_role:
            return {
                'mess': 'Role name already exists!',
                'status_code': status.HTTP_400_BAD_REQUEST
            }
        
        role = Role(
            role_name=request.role_name,
            role_description=request.role_description
        )
        db.add(role)
        db.flush()  
        
        if request.permissions:
            permissions = db.query(Permission).filter(
                Permission.permission_id.in_(request.permissions)
            ).all()
            
            if len(permissions) != len(request.permissions):
                return {
                    'mess': 'Some permissions not found!',
                    'status_code': status.HTTP_404_NOT_FOUND
                }
            
            for permission_id in request.permissions:
                role_permission = RolePermission(
                    role_id=role.role_id,
                    permission_id=permission_id
                )
                db.add(role_permission)
        
        db.commit()
        db.refresh(role)
        
        role_with_permissions = (
            db.query(Role)
            .options(joinedload(Role.role_permission).joinedload(RolePermission.permission))
            .filter(Role.role_id == role.role_id)
            .first()
        )
        
        permissions_data = []
        if role_with_permissions.role_permission:
            permissions_data = sorted([
                {
                    'permission_id': rp.permission.permission_id,
                    'permission_name': rp.permission.permission_name,
                    'description': rp.permission.permission_description
                }
                for rp in role_with_permissions.role_permission
            ], key=lambda x: x['permission_id'])
        
        role_data = {
            'role_id': role_with_permissions.role_id,
            'role_name': role_with_permissions.role_name,
            'description': role_with_permissions.role_description,
            'created_at': role_with_permissions.created_at,
            'created_by': role_with_permissions.created_by,
            'permissions': permissions_data
        }
        log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Create role",
			target_type= "Role"
		)
        
        return {
            'mess': 'Role created successfully with permissions!',
            'status_code': status.HTTP_201_CREATED,
            'data': role_data
        }
        
    except Exception as ex:
        db.rollback()
        return get_internal_server_error(ex)

async def get_roles(db: Session, logRequest: Request, current_user: dict):
    try:
        log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Get roles",
			target_type= "Role"
		)
        return {
            'mess' : 'Get all roles successfully !',
            'status_code' : status.HTTP_200_OK,
            'data' : db.query(Role).all()
        }
    except Exception as ex:
        return get_internal_server_error(ex)

async def get_role(db: Session, role_id: int, logRequest: Request, current_user: dict):
    try:
        role = (
            db.query(Role)
            .options(
                joinedload(Role.role_permission)
                .joinedload(RolePermission.permission)
                .joinedload(Permission.permission_type)  
            )
            .filter(Role.role_id == role_id)
            .first()
        )
        
        if not role:
            return {
                'mess': 'Role not found!',
                'status_code': status.HTTP_404_NOT_FOUND
            }
        
        permissions_data = []
        if role.role_permission:
            permissions_data = sorted([
                {
                    'permission_id': rp.permission.permission_id,
                    'permission_name': rp.permission.permission_name,
                    # 'description': rp.permission.description,
                    # 'permission_type_id': rp.permission.permission_type_id, 
                    'permission_type_name': rp.permission.permission_type.permission_type_name if rp.permission.permission_type else None  
                }
                for rp in role.role_permission
            ], key=lambda x: x['permission_id'])
        
        role_data = {
            'role_id': role.role_id,
            'role_name': role.role_name,
            'description': role.role_description,
            'created_at': role.created_at,
            'created_by': role.created_by,
            'updated_at': role.updated_at,
            'updated_by': role.updated_by,
            'permissions': permissions_data
        }
        log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Get role by id",
			target_type= "Role"
		)
        return {
            'mess': 'Role retrieved successfully!',
            'status_code': status.HTTP_200_OK,
            'data': role_data
        }
        
    except Exception as ex:
        return get_internal_server_error(ex)


async def update_role(db: Session, request: RoleUpdate, logRequest: Request, current_user: dict):
    try:
        permission = await check_permission(db, 'manage', 'role', current_user['role_id'])
        if not permission:
            return {
                'mess' : "You don't have permission for accessing this function !",
                'status_code' : status.HTTP_403_FORBIDDEN 
        }
        role = db.query(Role).filter(Role.role_id == request.role_id).first()
        if not role:
            return {
                'mess': 'Role not found!',
                'status_code': status.HTTP_404_NOT_FOUND
            }
        
        if request.role_name and request.role_name != role.role_name:
            existing_role = db.query(Role).filter(
                Role.role_name == request.role_name,
                Role.role_id != request.role_id
            ).first()
            if existing_role:
                return {
                    'mess': 'Role name already exists!',
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
        
        if request.role_name is not None:
            role.role_name = request.role_name
        if request.role_description is not None:
            role.role_description = request.role_description
        
        role.updated_at = datetime.utcnow()
        role.updated_by = current_user['user_name']  
        
        if request.permissions is not None:
            db.query(RolePermission).filter(RolePermission.role_id == request.role_id).delete()
            
            if request.permissions:
                permissions = db.query(Permission).filter(
                    Permission.permission_id.in_(request.permissions)
                ).all()
                
                if len(permissions) != len(request.permissions):
                    return {
                        'mess': 'Some permissions not found!',
                        'status_code': status.HTTP_404_NOT_FOUND
                    }
                
                for permission_id in request.permissions:
                    role_permission = RolePermission(
                        role_id=request.role_id,
                        permission_id=permission_id
                    )
                    db.add(role_permission)
        
        db.commit()
        db.refresh(role)
        
        updated_role = (
            db.query(Role)
            .options(joinedload(Role.role_permission).joinedload(RolePermission.permission))
            .filter(Role.role_id == request.role_id)
            .first()
        )
        
        permissions_data = []
        if updated_role.role_permission:
            permissions_data = sorted([
                {
                    'permission_id': rp.permission.permission_id,
                    'permission_name': rp.permission.permission_name,
                    'description': rp.permission.permission_description
                }
                for rp in updated_role.role_permission
            ], key=lambda x: x['permission_id'])
        
        role_data = {
            'role_id': updated_role.role_id,
            'role_name': updated_role.role_name,
            'description': updated_role.role_description,
            'created_at': updated_role.created_at,
            'created_by': updated_role.created_by,
            'updated_at': updated_role.updated_at,
            'updated_by': updated_role.updated_by,
            'permissions': permissions_data
        }
        log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Update role",
			target_type= "Role"
		)
        return {
            'mess': 'Role updated successfully!',
            'status_code': status.HTTP_200_OK,
            'data': role_data
        }
        
    except Exception as ex:
        db.rollback()
        return get_internal_server_error(ex)


async def delete_role(db: Session, role_id: int, logRequest: Request, current_user: dict):
    try:
        permission = await check_permission(db, 'manage', 'role', current_user['role_id'])
        if not permission:
            return {
                'mess' : "You don't have permission for accessing this function !",
                'status_code' : status.HTTP_403_FORBIDDEN 
        }
        role = db.query(Role).filter(Role.role_id == role_id).first()
        if not role:
            return {
                'mess': 'Role not found!',
                'status_code': status.HTTP_404_NOT_FOUND
            }
        
        # This code is userd for restricting to delete role which already has at least a user -> Disable at this time 
        # if role.users:
        #     return {
        #         'mess': 'Cannot delete role that is assigned to users!',
        #         'status_code': status.HTTP_400_BAD_REQUEST
        #     }
        
        db.delete(role)
        db.commit()
        log_activity(
			db=db,
			request= logRequest,
			user_id= current_user['user_id'],
			activity_description= "Delete role",
			target_type= "Role"
		)
        return {
            'mess': 'Role deleted successfully!',
            'status_code': status.HTTP_204_NO_CONTENT
        }
        
    except Exception as ex:
        db.rollback()
        return get_internal_server_error(ex)
