from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Permission(Base):
	__tablename__ = 'tb_permission'

	permission_id = Column(Integer, primary_key = True, index = True)
	permission_name = Column(String(100), nullable = False)
	permission_description = Column(String(255))
	permission_type_id = Column(Integer, ForeignKey('tb_permission_type.permission_type_id', ondelete='CASCADE'), nullable=False)
	created_at = Column(DateTime, default = datetime.utcnow)
	created_by = Column(String(50), default='admin')
	updated_at = Column(DateTime)
	updated_by = Column(String(50), default='admin')

	# Set relationship
	permission_type = relationship('PermissionType', back_populates='permissions')
	role_permission = relationship('RolePermission', back_populates='permission', cascade='all, delete-orphan')