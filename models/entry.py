from core.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from models import DataPoint


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

    def add_data_point(self, key, value):
        data_point = db.session.query(DataPoint).filter_by(entry_id=self.id, name=key).first()
        if not data_point:
            data_point = DataPoint(self, key)
            db.session.add(data_point)
        data_point.set_value(value)
        db.session.commit()

    def get_data_point(self, key):
        return next((data_point.get_value() for data_point in self.data_points if data_point.name == key), None)

    def get_financial_document(self):
        return next((doc for doc in self.documents if doc.label == self.year_obj.financial_label), None)

    def get_employee_document(self):
        return next((doc for doc in self.documents if doc.label == 'Personeel'), None)

    def get_entity_document(self):
        return next((doc for doc in self.documents if doc.label == 'Hoofdentiteit / Groepshoofd'), None)

    def get_necessary_documents(self):
        return [
            self.get_financial_document(),
            self.get_employee_document(),
            self.get_entity_document()
        ]

    def to_list(self, business_id=True, name=True, data_points=[]):
        row = []
        if business_id:
            row.append(self.business_id)
        if name:
            row.append(self.name)
        for data_point in data_points:
            row.append(self.get_data_point(data_point))
        return row
