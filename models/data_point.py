from core.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class DataPoint(db.Model):
    __tablename__ = 'data_points'

    id             = Column(Integer, primary_key=True)
    institution_id = Column(Integer, ForeignKey('institutions.id'))
    institution    = relationship('Institution', back_populates='data_points')
    year           = Column(Integer)
    name           = Column(String)
    value_type     = Column(String)
    value          = Column(String)
