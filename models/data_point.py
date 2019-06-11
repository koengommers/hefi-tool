from core.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class DataPoint(db.Model):
    __tablename__ = 'data_points'

    id             = Column(Integer, primary_key=True)
    entry_id       = Column(Integer, ForeignKey('entries.id'), nullable=False)
    entry          = relationship('Entry', back_populates='data_points')
    name           = Column(String)
    value_type     = Column(String)
    value          = Column(String)
