from sqlalchemy.orm import Session, joinedload
from app.models import Permission, Role, RolePermission
from app.schemas import RoleCreate, RoleUpdate
from datetime import datetime
from fastapi import HTTPException, status
from app.utils import get_internal_server_error

async def create_role(db: Session, request: RoleCreate):
    try:
        existing_role = db.query(Role).filter(Role.role_name == request.role_name).first()
        if existing_role:
            return {
                'mess': 'Role name already exists!',
                'status_code': status.HTTP_400_BAD_REQUEST
            }
        
        role = Role(
            role_name=request.role_name,
            description=request.description
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
                    'description': rp.permission.description
                }
                for rp in role_with_permissions.role_permission
            ], key=lambda x: x['permission_id'])
        
        role_data = {
            'role_id': role_with_permissions.role_id,
            'role_name': role_with_permissions.role_name,
            'description': role_with_permissions.description,
            'created_at': role_with_permissions.created_at,
            'created_by': role_with_permissions.created_by,
            'permissions': permissions_data
        }
        
        return {
            'mess': 'Role created successfully with permissions!',
            'status_code': status.HTTP_201_CREATED,
            'data': role_data
        }
        
    except Exception as ex:
        db.rollback()
        return get_internal_server_error(ex)


async def get_role(db: Session, role_id: int):
    try:
        role = (
            db.query(Role)
            .options(joinedload(Role.role_permission).joinedload(RolePermission.permission))
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
                    'description': rp.permission.description
                }
                for rp in role.role_permission
            ], key=lambda x: x['permission_id'])
        
        role_data = {
            'role_id': role.role_id,
            'role_name': role.role_name,
            'description': role.description,
            'created_at': role.created_at,
            'created_by': role.created_by,
            'updated_at': role.updated_at,
            'updated_by': role.updated_by,
            'permissions': permissions_data
        }
        
        return {
            'mess': 'Role retrieved successfully!',
            'status_code': status.HTTP_200_OK,
            'data': role_data
        }
        
    except Exception as ex:
        return get_internal_server_error(ex)


async def get_roles(db: Session, skip: int = 0, limit: int = 100):
    try:
        roles = (
            db.query(Role)
            .options(joinedload(Role.role_permission).joinedload(RolePermission.permission))
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        roles_data = []
        for role in roles:
            permissions_data = []
            if role.role_permission:
                permissions_data = sorted([
                    {
                        'permission_id': rp.permission.permission_id,
                        'permission_name': rp.permission.permission_name,
                        'description': rp.permission.description
                    }
                    for rp in role.role_permission
                ], key=lambda x: x['permission_id'])
            
            role_data = {
                'role_id': role.role_id,
                'role_name': role.role_name,
                'description': role.description,
                'created_at': role.created_at,
                'created_by': role.created_by,
                'updated_at': role.updated_at,
                'updated_by': role.updated_by,
                'permissions': permissions_data
            }
            roles_data.append(role_data)
        
        roles_data.sort(key=lambda x: x['role_id'])
        
        return {
            'mess': 'Roles retrieved successfully!',
            'status_code': status.HTTP_200_OK,
            'data': roles_data,
            'total': len(roles_data)
        }
        
    except Exception as ex:
        return get_internal_server_error(ex)


async def update_role(db: Session, request: RoleUpdate):
    try:
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
        if request.description is not None:
            role.description = request.description
        
        role.updated_at = datetime.utcnow()
        role.updated_by = 'admin'  
        
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
                    'description': rp.permission.description
                }
                for rp in updated_role.role_permission
            ], key=lambda x: x['permission_id'])
        
        role_data = {
            'role_id': updated_role.role_id,
            'role_name': updated_role.role_name,
            'description': updated_role.description,
            'created_at': updated_role.created_at,
            'created_by': updated_role.created_by,
            'updated_at': updated_role.updated_at,
            'updated_by': updated_role.updated_by,
            'permissions': permissions_data
        }
        
        return {
            'mess': 'Role updated successfully!',
            'status_code': status.HTTP_200_OK,
            'data': role_data
        }
        
    except Exception as ex:
        db.rollback()
        return get_internal_server_error(ex)


async def delete_role(db: Session, role_id: int):
    try:
        role = db.query(Role).filter(Role.role_id == role_id).first()
        if not role:
            return {
                'mess': 'Role not found!',
                'status_code': status.HTTP_404_NOT_FOUND
            }
        
        if role.users:
            return {
                'mess': 'Cannot delete role that is assigned to users!',
                'status_code': status.HTTP_400_BAD_REQUEST
            }
        
        db.delete(role)
        db.commit()
        
        return {
            'mess': 'Role deleted successfully!',
            'status_code': status.HTTP_200_OK
        }
        
    except Exception as ex:
        db.rollback()
        return get_internal_server_error(ex)
    
async def get_permission_by_role(db: Session, role_id : int):
    try:
        pass
    except Exception as ex:
        return get_internal_server_error(ex)