from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from db import Base

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    balance = Column(Float, default=0)
    ccy = Column(String(3), nullable=False, default='EUR')
    limit = Column(Float, default=0)
    ops = relationship("Transaction")

class Transaction(Base):

    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey('account.id'))
    op_type = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    ccy = Column(String(3), nullable=False)
    date = Column(DateTime)
    op_details = Column(String(250))

