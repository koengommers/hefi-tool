from core.database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Year(db.Model):
    __tablename__ = 'years'

    year       = Column(Integer, primary_key=True)
    digimv_url = Column(String)
    entries    = relationship('Entry', back_populates='year_obj')
