from core.database import db
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Document(db.Model):
    __tablename__ = 'documents'

    id             = Column(Integer, primary_key=True)
    institution_id = Column(Integer, ForeignKey('institutions.id'))
    institution    = relationship('Institution', back_populates='documents')
    label          = Column(String)
    standardized   = Column(Boolean)
    name           = Column(String)
    year           = Column(Integer)
    downloaded     = Column(Boolean, default=False)
    downloaded_on  = Column(DateTime)
    indexed_on     = Column(DateTime)
    published_on   = Column(Date)
    path           = Column(String)
