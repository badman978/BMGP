from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
#
#

class Produce(Base):
    __tablename__ = 'produce'

    id = Column(Integer, primary_key=True, nullable=False)
    farm_produce = Column(String, nullable=False) 
    qty = Column(Integer, nullable=False) 
    on_sale = Column(Boolean, nullable=False, server_default='False')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    farm = Column(String,ForeignKey("farms.username", ondelete="CASCADE") ,nullable=False)

    farmer = relationship("Farms")

class Farms(Base):
    __tablename__ = 'farms'
    id = Column(Integer, primary_key=True, nullable=False, index = True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))









     