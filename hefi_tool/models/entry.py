"""Contains Entry class."""

from ..database import db
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..models import DataPoint


class Entry(db.Model):
    """Represents an entry of an institution.

    An entry is a unique combination of institution and year.
    This class is a SQLAlchemy model for the database.

    """

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
        """Store a new entry.

        Args:
            business_id (str): The business id of the institution (KvK nummer).
            year (int): The year of the entry.
            name (str): Name of the institution.
            location (str): Geographical location of the institution.

        """
        self.business_id = business_id
        self.year = year
        self.name = name
        self.location = location

    def add_data_point(self, key, value):
        """Add data point to this entry.

        Args:
            key (str): Key/name of the data point.
            value: Value of the data point.

        """
        data_point = db.session.query(DataPoint).filter_by(entry_id=self.id, name=key).first()
        if not data_point:
            data_point = DataPoint(self, key)
            db.session.add(data_point)
        data_point.set_value(value)
        db.session.commit()

    def get_data_point(self, key):
        """Get a data point by key.

        Args:
            key (str): Key of the data point.

        Returns:
            value of the data point.

        """
        return next((data_point.get_value() for data_point in self.data_points if data_point.name == key), None)

    def get_financial_document(self):
        """Get the financial document of this entry.

        Returns:
            (Document) The financial document.

        """
        return next((doc for doc in self.documents if self.year_obj.financial_label.lower() in doc.label.lower()), None)

    def get_employee_document(self):
        """Get the employee document of this entry.

        Returns:
            (Document) The employee document.

        """
        return next((doc for doc in self.documents if doc.label == 'Personeel'), None)

    def get_entity_document(self):
        """Get the entity document of this entry.

        Returns:
            (Document) The entity document.

        """
        return next((doc for doc in self.documents if doc.label == 'Hoofdentiteit / Groepshoofd'), None)

    def get_necessary_documents(self):
        """Get all documents needed for data extraction.

        Returns:
            (list) List of documents.

        """
        return [
            self.get_financial_document(),
            self.get_employee_document(),
            self.get_entity_document()
        ]

    def to_list(self, business_id=True, name=True, data_points=[]):
        """Convert this entry in a list containing data points.

        Is used for putting data in a DataFrame.

        Args:
            business_id (bool): Whether the business id needs to be included.
            name (bool): Whether the institution name needs to be included.
            data_points (list): List of data point keys that need to be included.

        Returns:
            (list) List of entry properties and data points.

        """
        row = []
        if business_id:
            row.append(self.business_id)
        if name:
            row.append(self.name)
        for data_point in data_points:
            row.append(self.get_data_point(data_point))
        return row
