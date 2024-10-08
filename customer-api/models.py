from sqlalchemy import Column, String, Integer
from .database import Base

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(50))

    def __repr__(self):
        return f"<Customer(name={self.full_name}, email={self.email})>"
