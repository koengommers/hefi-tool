from core.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Entry(db.Model):
    __tablename__ = 'entries'

    id          = Column(Integer, primary_key=True)
    business_id = Column(String, nullable=False)
    name        = Column(String)
    location    = Column(String)
    year        = Column(Integer, ForeignKey('years.year'), nullable=False)
    year_obj    = relationship('Year', back_populates='entries')
    documents   = relationship('Document', back_populates='entry')
    data_points = relationship('DataPoint', back_populates='entry')

    # unique combination of year and business_id
    __table_args__ = (UniqueConstraint('business_id', 'year'),)

    def __init__(self, business_id, year, name, location):
        self.business_id = business_id
        self.year = year
        self.name = name
        self.location = location
