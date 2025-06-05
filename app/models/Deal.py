from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey
from datetime import datetime
from app.db.base import Base
from sqlalchemy.orm import relationship

class Deal(Base):
	__tablename__ = 'tb_deal'

	deal_id = Column(Integer, primary_key=True, index=True)
	deal_type = Column(String(50))
	description = Column(String(255))
	user_id = Column(Integer, ForeignKey('tb_user.user_id'), nullable=False)
	tax_indentification_number = Column(String(50))
	customer_name = Column(String(100))
	domain_name = Column(String(50))
	status = Column(String(50), default = 'draft')
	contact_name = Column(String(255), nullable = False, default='')
	contact_email = Column(String(255), nullable = False, default='')
	contact_phone = Column(String(255), nullable = False, default='')
	address = Column(String(255))
	billing_address = Column(String(255))
	created_at = Column(DateTime, default = datetime.utcnow)
	created_by = Column(String(50))
	updated_at = Column(DateTime)
	updated_by = Column(String(50))

	# Set relationship
	user = relationship('User', back_populates='deals')
	orders = relationship('Order', back_populates='deal', cascade='all, delete-orphan')
