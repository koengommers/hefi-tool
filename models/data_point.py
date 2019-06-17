from core.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class DataPoint(db.Model):
    __tablename__ = 'data_points'

    id             = Column(Integer, primary_key=True)
    entry_id       = Column(Integer, ForeignKey('entries.id'), nullable=False)
    entry          = relationship('Entry', back_populates='data_points')
    name           = Column(String)
    value_type     = Column(String)
    value          = Column(String)

    def __init__(self, entry, key):
        self.entry = entry
        self.name = key

    def set_value(self, value):
        if type(value) == int:
            self.value_type = 'integer'
        elif type(value) == float:
            self.value_type = 'float'
        elif type(value) == str:
            self.value_type = 'string'
        elif type(value) == bool:
            self.value_type = 'boolean'
        if value is not None:
            value = str(value)
        self.value = value

    def get_value(self):
        value = self.value
        if self.value_type == 'integer':
            value = int(value)
        elif self.value_type == 'float':
            value = float(value)
        elif self.value_type == 'boolean':
            value = value == 'True'
        return value
