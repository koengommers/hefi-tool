"""Contains Database class and starts database session."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


DB_URL = 'sqlite:///data/database.sqlite'


class Database:
    """Wrapper class for access to the database."""

    def __init__(self, url):
        """Start a new session.

        Args:
            url (str): URL for database connection.

        """
        self.engine = create_engine(url)
        self.Model = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_all(self):
        """Create all tables and columns."""
        self.Model.metadata.create_all(self.engine)


db = Database(DB_URL)
