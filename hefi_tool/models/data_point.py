"""Contains DataPoint class."""

from ..database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class DataPoint(db.Model):
    """Represents a data point.

    This class is a SQLAlchemy model for the database.
    A data point is stored with a key/name, a value type and value.

    """

    __tablename__ = 'data_points'

    id             = Column(Integer, primary_key=True)
    entry_id       = Column(Integer, ForeignKey('entries.id'), nullable=False)
    entry          = relationship('Entry', back_populates='data_points')
    name           = Column(String)
    value_type     = Column(String)
    value          = Column(String)

    def __init__(self, entry, key):
        """Create a new data point.

        Args:
            entry (Entry): The entry to which the data point belongs.
            key (str): The key/name for the data point.

        """
        self.entry = entry
        self.name = key

    @staticmethod
    def list_to_csv(value):
        """Convert a list to a comma separated string.

        Args:
            value (list): The list to convert.

        """
        return ', '.join(map(lambda x: '"{}"'.format(str(x).replace('"', '')), value))

    def set_value(self, value):
        """Set the value of the data point.

        The value type is inferred from the value variable type.

        Args:
            value: The value to set.

        """
        if type(value) == int:
            self.value_type = 'integer'
        elif type(value) == float:
            self.value_type = 'float'
        elif type(value) == str:
            self.value_type = 'string'
        elif type(value) == bool:
            self.value_type = 'boolean'
        elif type(value) == list:
            self.value_type = 'list'
            value = self.list_to_csv(value)
        if value is not None:
            value = str(value)
        self.value = value

    def get_value(self):
        """Get the value from the data point.

        The value is converted to fit its value type.

        """
        value = self.value
        if self.value is None:
            return self.value
        elif self.value_type == 'integer':
            value = int(value)
        elif self.value_type == 'float':
            value = float(value)
        elif self.value_type == 'boolean':
            value = value == 'True'
        return value
