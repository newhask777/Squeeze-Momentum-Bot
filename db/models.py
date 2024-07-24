from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, JSON, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped
from db.conn import Base
from typing import Dict
import datetime


# PREDICTIONS
class WsCandle(Base):
    __tablename__ = "ws"

    id = Column(Integer, primary_key=True, index=True)
    open = Column(String(255))
    high = Column(String(255))
    low = Column(String(255))
    close = Column(String(255))
    volume = Column(String(255))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

class HttpCandle(Base):
    __tablename__ = "http"

    id = Column(Integer, primary_key=True, index=True)
    stamp = Column(String(255))
    open = Column(String(255))
    high = Column(String(255))
    low = Column(String(255))
    close = Column(String(255))
    volume = Column(String(255))


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}