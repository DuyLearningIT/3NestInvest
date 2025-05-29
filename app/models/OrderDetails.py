from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class OrderDetails(Base):
    __tablename__ = 'tb_order_details'

    order_details_id = Column(Integer, primary_key=True, index = True)
    order_id = Column(Integer, ForeignKey("tb_order.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("tb_product.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price_for_customer = Column(Float, default = 0)
    final_price = Column(Float, default = 0)
    service_contract_duration = Column(Integer, default=1)
    
    # Set relationship
    order = relationship('Order', back_populates='order_details')
    product = relationship('Product', back_populates='order_details')