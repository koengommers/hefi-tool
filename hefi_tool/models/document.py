"""Contains Database class."""

import os
import string
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import db
from ..retrieval.document_downloader import DocumentDownloader


class Document(db.Model):
    """Represents a document.

    This class is a SQLAlchemy model for the database.

    """

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
    is_processed   = Column(Boolean, default=False)

    def __init__(self, entry, label, standardized, name=None, published_on=None, url=None):
        """Create a new document.

        Args:
            entry (Entry): The entry to which the document belongs.
            label (str): The label the document has.
            standardized (bool): Whether the document is a standardized format.
            name (str): The optional name of the document.
            published_on (datetime.date): Date on which it was published.
            url (str): Optional url to the document.
                The URL isn't really used, because it is generated
                and not reliable because it changes.

        """
        self.entry = entry
        self.label = label
        self.standardized = standardized
        self.name = name
        self.published_on = published_on
        self.url = url

    def filename(self, ext=True):
        """Get the filename for storing the document.

        Args:
            ext (bool): Whether to include the extension (.pdf)

        Returns:
            (str) The filename.

        """
        template = '{}-{}-{}'
        if ext:
            template += '.pdf'
        valid_filename_chars = '-_.() ' + string.ascii_letters + string.digits
        clean_label = ''.join(c for c in self.label if c in valid_filename_chars)
        return template.format(clean_label, self.entry.business_id, self.entry.year)

    def get_path(self, download=True):
        """Get path of the document file.

        Args:
            download (bool): Whether to download document if it isn't yet.

        Returns:
            (str) The absolute path to the file.

        """
        if download and not self.downloaded:
            self.download()
        if self.path:
            return os.path.join(os.path.abspath('data/pdf'), self.path)
        return None

    def set_downloaded(self):
        """Mark the document as downloaded and save path."""
        self.path = self.filename()
        self.downloaded = True
        self.downloaded_on = datetime.utcnow()
        db.session.commit()

    def remove_download(self):
        """Unmark the document as downloaded."""
        self.path = None
        self.downloaded = False
        self.downloaded_on = None
        db.session.commit()

    def download(self):
        """Download this document."""
        downloader = DocumentDownloader([self])
        downloader.download()

    def set_processed(self):
        """Mark the document as processed."""
        self.is_processed = True
        db.session.commit()
