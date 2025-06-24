from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Category(Base):
	__tablename__ ='tb_category'

	category_id = Column(Integer, primary_key = True, index=True)
	category_name = Column(String(100), unique = True, nullable = False)
	type_id = Column(Integer, ForeignKey('tb_type.type_id'), nullable=False)
	category_description  = Column(String(255))
	created_at = Column(DateTime, default = datetime.utcnow)
	created_by = Column(String(50), default='admin')
	updated_at = Column(DateTime)
	updated_by = Column(String(50), default='admin')

	# Set relationship
	products = relationship("Product", back_populates='category', cascade='all, delete-orphan', passive_deletes=True)
	tb_type = relationship("Type", back_populates='category')