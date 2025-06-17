from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class RolePermission(Base):
	__tablename__ = 'tb_role_permission'

	role_permission_id = Column(Integer, primary_key=True, index = True)
	role_id = Column(Integer, ForeignKey("tb_role.role_id"), nullable=False)
	permission_id = Column(Integer, ForeignKey("tb_permission.permission_id"), nullable=False)
    
	# Set relationship
	role = relationship('Role', back_populates='role_permission')
	permission = relationship('Permission', back_populates='role_permission')