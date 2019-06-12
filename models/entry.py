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

    @staticmethod
    def bulk_process(entries)
        necessary_documents = []
        for entry in entries:
            necessary_documents += entry.get_necessary_documents()
        Document.bulk_download(necessary_documents)

        for entry in entries:
            entry.get_data()

    def process(self):
        necessary_documents = self.get_necessary_documents()
        Document.bulk_download(necessary_documents)
        self.get_data()

    def get_necessary_documents(self):
        pass

    def get_data(self):
        self.get_finance_data()
        self.get_personnel_data()

    def add_data_point(self, key, value, value_type):
        pass

    def get_finance_data(self):
        finance_document = self.get_financial_document()
        extractor = FinanceDataExtractor(finance_document)
        results = extractor.get_results()
        for key, value in results.items():
            value_type = 'integer'
            self.add_data_point(self, key, value, value_type)

    def get_personnel_data(self):
        pass
