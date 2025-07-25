from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    amount = Column(Float)
    description = Column(String, nullable=True)
