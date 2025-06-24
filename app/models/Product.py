from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Product(Base):
	__tablename__ = 'tb_product'

	product_id = Column(Integer, primary_key=True, index=True)
	product_name = Column(String(255), unique=True, nullable=False)
	product_role = Column(Integer, ForeignKey('tb_role.role_id'), nullable=False)
	category_id = Column(Integer, ForeignKey('tb_category.category_id', ondelete='CASCADE'), nullable=False)
	product_description = Column(String(255))
	sku_partnumber = Column(String(100)) # It's a kind of product number
	price = Column(Float, nullable=False)
	channel_cost = Column(Float, default= 0) # This means how much money does the business have to pay for us
	maximum_discount = Column(Float, default = 0)
	maximum_discount_price = Column(Float, default = price - ( maximum_discount * price / 100 ))
	status = Column(Boolean, default = True)
	created_at = Column(DateTime, default = datetime.utcnow)
	created_by = Column(String(50), default='admin')
	updated_at = Column(DateTime)
	updated_by = Column(String(50), default='admin')

	# set relationship
	category = relationship('Category', back_populates='products')
	order_details = relationship('OrderDetails', back_populates='product', passive_deletes=True)
	role = relationship('Role', back_populates='products')