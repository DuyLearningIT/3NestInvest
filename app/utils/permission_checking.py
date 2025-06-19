# from app.crud.permission import get_permissions_by_role
from sqlalchemy.orm import Session, joinedload
from app.utils import get_internal_server_error
from app.models import Role, Permission, RolePermission
from app.schemas import PermissionCreate, PermissionUpdate
from fastapi import HTTPException, status
from app.utils import get_internal_server_error, get_permission_type_or_404, get_permission_or_404


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

async def check_permission(db: Session, per: str, permission_type: str, role_id: int) -> bool:
	response = await get_permissions_by_role(db, role_id)
	permissions = response['data']['permissions']
	for permission in permissions:
		if permission['permission_type_name'].strip().lower() == permission_type.strip().lower():
			if permission['permission_name'].strip().lower() == 'Full control'.strip().lower() or permission['permission_name'].strip().lower() == per.strip().lower():
				return True
	return False
