from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey
from datetime import datetime
from app.db.base import Base
from sqlalchemy.orm import relationship

class Order(Base):
	__tablename__ = 'tb_order'

	order_id = Column(Integer, primary_key=True, index=True)
	customer_name = Column(String(50))
	status = Column(String(50), default = 'draft')
	order_title = Column(String(255))
	user_id = Column(Integer, ForeignKey('tb_user.user_id'), nullable=False)
	total_budget = Column(Float, default = 0)
	created_at = Column(DateTime, default = datetime.utcnow)
	created_by = Column(String(50))
	updated_at = Column(DateTime)
	updated_by = Column(String(50))

	# Set relationship
	user = relationship('User', back_populates='orders')
	order_details = relationship('OrderDetails', back_populates='order')