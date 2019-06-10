from core.database import db
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Document(db.Model):
    __tablename__ = 'documents'

    id             = Column(Integer, primary_key=True)
    entry_id       = Column(Integer, ForeignKey('entries.id'))
    entry          = relationship('Entry', back_populates='documents')
    label          = Column(String)
    standardized   = Column(Boolean)
    name           = Column(String)
    downloaded     = Column(Boolean, default=False)
    downloaded_on  = Column(DateTime)
    indexed_on     = Column(DateTime)
    published_on   = Column(Date)
    url            = Column(String)
    path           = Column(String)
