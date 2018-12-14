from db import Base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship, backref
import datetime

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    amount = Column(Float, default=0)
    curency = Column(String(3), nullable=False)
    created = Column(DateTime, default=datetime.date.today())
    limit = Column(Float, default=0)

    def __repr__(self):
        return "<Account {} ::: Amount {} ::: Curency {}>".format(self.name, self.amount, self.curency)