"""Contains Year class."""

from ..database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Year(db.Model):
    """Represents a year.

    This class is a SQLAlchemy model for the database.

    """

    __tablename__ = 'years'

    year            = Column(Integer, primary_key=True)
    digimv_url      = Column(String)
    entries         = relationship('Entry', back_populates='year_obj')
    financial_label = Column(String, default='Financiële gegevens')

    def __init__(self, year, digimv_url):
        """Add a new year.

        Args:
            year (int): The year.
            digimv_url (str): Base url for the standardized documents.
        """
        self.year = year
        self.digimv_url = digimv_url
