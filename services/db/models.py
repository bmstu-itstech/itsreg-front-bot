from datetime import datetime
from sqlalchemy import Column, BigInteger, Integer, DateTime, Time, Boolean, Text


from services.db.base import Base


class BaseCommon(Base):
    __abstract__ = True

    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class User(BaseCommon):    
    __tablename__ = "users"

    uuid = Column(BigInteger, primary_key=True)                  # it is also pseudo email
    pseudo_password = Column(Text)                                     # timestamp
    token = Column(Text, nullable=True)


class ItsBot(BaseCommon):
    __tablename__ = "its_bots"

    uuid = Column(Text, primary_key=True)
    token = Column(Text)
    name = Column(Text)
