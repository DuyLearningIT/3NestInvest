from sqlalchemy.orm import Session, joinedload
from app.models import PermissionType, Permission, Role, RolePermission
from app.schemas import PermissionCreate, PermissionUpdate
from datetime import datetime
from fastapi import HTTPException, status
from app.utils import get_internal_server_error, get_permission_type_or_404, get_permission_or_404
# from app.utils.permission_checking import check_permission

async def create_permission(db: Session, request: PermissionCreate):
    try:
        existing_permission = db.query(Permission).filter(
            Permission.permission_name == request.permission_name
        ).first()
        
        if existing_permission:
            return {
                'mess': 'Permission has already existed!',
                'status_code': status.HTTP_400_BAD_REQUEST
            }
        
        permission_type = get_permission_type_or_404(db, request.permission_type_id)
        
        permission = Permission(
            permission_name=request.permission_name,
            permission_description=request.permission_description,
            permission_type_id=request.permission_type_id
        )
        
        db.add(permission)
        db.commit()
        db.refresh(permission)
        
        permission_with_type = (
            db.query(Permission)
            .options(joinedload(Permission.permission_type))
            .filter(Permission.permission_id == permission.permission_id)
            .first()
        )
        
        permission_data = {
            'permission_id': permission_with_type.permission_id,
            'permission_name': permission_with_type.permission_name,
            'description': permission_with_type.permission_description,
            'permission_type_id': permission_with_type.permission_type_id,
            'permission_type_name': permission_with_type.permission_type.permission_type_name,
            'created_at': permission_with_type.created_at,
            'created_by': permission_with_type.created_by
        }
        
        return {
            'mess': 'Add permission successfully!',
            'status_code': status.HTTP_201_CREATED,
            'data': permission_data
        }
    except Exception as ex:
        return get_internal_server_error(ex)


async def get_permissions(db: Session):
    try:
        # permissions = (
        #     db.query(Permission)
        #     .options(joinedload(Permission.permission_type))
        #     .all()
        # )
        permissions = db.query(Permission, PermissionType.permission_type_id, PermissionType.permission_type_name) \
                        .join(PermissionType, PermissionType.permission_type_id == Permission.permission_type_id)  \
                        .all()
    
        permissions_data = [
                {
                    'permission_id': perm.permission_id,
                    'permission_name': perm.permission_name,
                    'description': perm.permission_description,
                    'permission_type_id': permission_type_id,
                    'permission_type_name': permission_type_name,
                    'created_at': perm.created_at,
                    'created_by': perm.created_by,
                    'updated_at': perm.updated_at,
                    'updated_by': perm.updated_by
                }
                for perm, permission_type_id, permission_type_name in permissions
            ]
        return {
            'mess': 'Get all permissions successfully!',
            'status_code': status.HTTP_200_OK,
            'data': permissions_data
        }
    except Exception as ex:
        return get_internal_server_error(ex)


async def get_permission(db: Session, request_id):
    try:
        permission = (
            db.query(Permission)
            .options(joinedload(Permission.permission_type))
            .filter(Permission.permission_id == request_id)
            .first()
        )
        
        if not permission:
            return {
                'mess': 'Permission not found!',
                'status_code': status.HTTP_404_NOT_FOUND
            }
        
        permission_data = {
            'permission_id': permission.permission_id,
            'permission_name': permission.permission_name,
            'description': permission.permission_description,
            'permission_type_id': permission.permission_type_id,
            'permission_type_name': permission.permission_type.permission_type_name,
            'created_at': permission.created_at,
            'created_by': permission.created_by,
            'updated_at': permission.updated_at,
            'updated_by': permission.updated_by
        }
        
        return {
            'mess': 'Get permission successfully!',
            'status_code': status.HTTP_200_OK,
            'data': permission_data
        }
    except Exception as ex:
        return get_internal_server_error(ex)


async def get_permissions_by_type(db: Session, request_id):
    try:
        permissions = (
            db.query(Permission)
            .options(joinedload(Permission.permission_type))
            .filter(Permission.permission_type_id == request_id)
            .all()
        )
        
        if not permissions:
            return {
                'mess': 'No permissions found for this permission type!',
                'status_code': status.HTTP_404_NOT_FOUND
            }
        
        permissions_data = [
            {
                'permission_id': perm.permission_id,
                'permission_name': perm.permission_name,
                'description': perm.permission_description,
                'permission_type_id': perm.permission_type_id,
                'permission_type_name': perm.permission_type.permission_type_name,
                'created_at': perm.created_at,
                'created_by': perm.created_by,
                'updated_at': perm.updated_at,
                'updated_by': perm.updated_by
            }
            for perm in permissions
        ]
        
        return {
            'mess': 'Get permissions by permission type successfully!',
            'status_code': status.HTTP_200_OK,
            'data': permissions_data
        }
    except Exception as ex:
        return get_internal_server_error(ex)


async def update_permission(db: Session, request: PermissionUpdate):
    try:
        permission = db.query(Permission).filter(
            Permission.permission_id == request.permission_id
        ).first()
        
        if not permission:
            return {
                'mess': 'Permission not found!',
                'status_code': status.HTTP_404_NOT_FOUND
            }
        
        if request.permission_name and request.permission_name != permission.permission_name:
            existing_permission = db.query(Permission).filter(
                Permission.permission_name == request.permission_name,
                Permission.permission_id != request.permission_id
            ).first()
            
            if existing_permission:
                return {
                    'mess': 'Permission name already exists!',
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
        
        if request.permission_type_id and request.permission_type_id != permission.permission_type_id:
            permission_type = db.query(PermissionType).filter(
                PermissionType.permission_type_id == request.permission_type_id
            ).first()
            
            if not permission_type:
                return {
                    'mess': 'Permission type not found!',
                    'status_code': status.HTTP_404_NOT_FOUND
                }
        
        if request.permission_name:
            permission.permission_name = request.permission_name
        if request.permission_description:
            permission.permission_description = request.permission_description
        if request.permission_type_id:
            permission.permission_type_id = request.permission_type_id
        permission.updated_at = datetime.now()
        permission.updated_by = 'admin' # Now is fixed because we don't have any accounts 
        
        db.commit()
        db.refresh(permission)
        
        updated_permission = (
            db.query(Permission)
            .options(joinedload(Permission.permission_type))
            .filter(Permission.permission_id == permission.permission_id)
            .first()
        )
        
        permission_data = {
            'permission_id': updated_permission.permission_id,
            'permission_name': updated_permission.permission_name,
            'description': updated_permission.permission_description,
            'permission_type_id': updated_permission.permission_type_id,
            'permission_type_name': updated_permission.permission_type.permission_type_name,
            'created_at': updated_permission.created_at,
            'created_by': updated_permission.created_by,
            'updated_at': updated_permission.updated_at,
            'updated_by': updated_permission.updated_by
        }
        
        return {
            'mess': 'Update permission successfully!',
            'status_code': status.HTTP_200_OK,
            'data': permission_data
        }
    except Exception as ex:
        return get_internal_server_error(ex)


async def delete_permission(db: Session, request_id):
    try:
        permission = db.query(Permission).filter(
            Permission.permission_id == request_id
        ).first()
        
        if not permission:
            return {
                'mess': 'Permission not found!',
                'status_code': status.HTTP_404_NOT_FOUND
            }
        
        db.delete(permission)
        db.commit()
        
        return {
            'mess': 'Delete permission successfully!',
            'status_code': status.HTTP_204_NO_CONTENT
        }
    except Exception as ex:
        return get_internal_server_error(ex)

async def get_permissions_by_role(db: Session, role_id: int):
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
        
        permissions_data = {
            'role_name': role.role_name,
            'permissions': permissions_data
        }
        
        return {
            'mess': 'Permissions retrieved by role successfully!',
            'status_code': status.HTTP_200_OK,
            'data': permissions_data
        }
    except Exception as ex:
        return get_internal_server_error(ex)