from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


DB_URL = 'sqlite:///data/database.sqlite'


class Database:

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Model = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_all(self):
        self.Model.metadata.create_all(self.engine)


db = Database(DB_URL)
