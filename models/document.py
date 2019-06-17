import os
import string
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import db
from pipeline.retrieval.document_downloader import DocumentDownloader


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

    def __init__(self, entry, label, standardized, name=None, published_on=None, url=None):
        self.entry = entry
        self.label = label
        self.standardized = standardized
        self.name = name
        self.published_on = published_on
        self.url = url

    def filename(self, ext=True):
        template = '{}-{}-{}'
        if ext:
            template += '.pdf'
        valid_filename_chars = '-_.() ' + string.ascii_letters + string.digits
        clean_label = ''.join(c for c in self.label if c in valid_filename_chars)
        return template.format(clean_label, self.entry.business_id, self.entry.year)

    def get_path(self):
        if not self.downloaded:
            self.download()
        return os.path.join(os.path.abspath('data/pdf'), self.path)

    def set_downloaded(self):
        self.path = self.filename()
        self.downloaded = True
        self.downloaded_on = datetime.utcnow()
        db.session.commit()

    def remove_download(self):
        self.path = None
        self.downloaded = False
        self.downloaded_on = None
        db.session.commit()

    def download(self):
        downloader = DocumentDownloader([self])
        downloader.download()
