from core.database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Institution(db.Model):
    __tablename__ = 'institutions'

    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    business_id = Column(String, unique=True)
    location    = Column(String)
    documents   = relationship('Document', back_populates='institution')
    data_points = relationship('DataPoint', back_populates='institution')

    def __init__(self, name, business_id, location):
        self.name = name
        self.business_id = business_id
        self.location = location
