from core.database import db
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Document(db.Model):
    __tablename__ = 'documents'

    id             = Column(Integer, primary_key=True)
    entry_id       = Column(Integer, ForeignKey('entries.id'), nullable=False)
    entry          = relationship('Entry', back_populates='documents')
    label          = Column(String)
    standardized   = Column(Boolean)
    name           = Column(String)
    downloaded     = Column(Boolean, default=False)
    downloaded_on  = Column(DateTime)
    indexed_on     = Column(DateTime, default=datetime.utcnow)
    published_on   = Column(Date)
    url            = Column(String)
    path           = Column(String)

    def __init__(self, entry, label, name, standardized, published_on, url=None):
        self.entry = entry
        self.label = label
        self.name = name
        self.standardized = standardized
        self.published_on = published_on
        self.url = url
