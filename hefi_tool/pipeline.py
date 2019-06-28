"""Contains Pipeline class.

The pipeline class is the entrypoint for running most processes
for data retrieval, data processing and also for data exporting.

"""

import pandas as pd
from sqlalchemy import func

from .database import db
from .models import Entry
from .processing.finance_data_extractor import FinanceDataExtractor
from .processing.entity_data_extractor import EntityDataExtractor
from .processing.employee_data_extractor import EmployeeDataExtractor
from .retrieval.document_downloader import DocumentDownloader
from .retrieval.document_scraper import DocumentScraper
from .retrieval.documents_page import DocumentsPage
from .retrieval.entry_scraper import EntryScraper
from .retrieval.overview_page import OverviewPage

class Pipeline:
    """Entry point for running data related tasks.

    It can:
    - process all entries from a given year
    - create financial details index file
    - export data points from a year to a DataFrame

    """

    @classmethod
    def process_year(cls, year, index_file):
        """Process a year.

        Args:
            year (int): The year to process.
            index_file (str): Path to a financial details index file.

        """
        cls.scrape_entries(year)

        entries = cls.get_entries(year)
        cls.index_standardized_documents(entries)
        cls.download_documents(entries)
        cls.extract_data(entries, index_file)

    @classmethod
    def get_entries(cls, year):
        """Get entries from a given year.

        Args:
            year (int): The year to get entries from.

        Returns:
            list: List of Entry objects.

        """
        return db.session.query(Entry).filter_by(year=year).all()

    @classmethod
    def year_to_dataframe(cls, year, business_id=None, name=None, data_points=[]):
        """Put data points from a year in a DataFrame.

        Args:
            year (int): The year to select data points from.
            business_id (str): The name of the business id column if it needs to be included.
            name (str): The name of the business name column if it needs to be included.
            data_points (list): List of data point keys that need to be included.

        Returns:
            The DataFrame.

        """
        entries = db.session.query(Entry).filter_by(year=year).all()
        return cls.entries_to_dataframe(entries, business_id, name, data_points)

    @classmethod
    def entries_to_dataframe(cls, entries, business_id=None, name=None, data_points=[]):
        """Put data points from certain entries in a DataFrame.

        Args:
            entries (list): List of Entry objects of which the data points get selected.
            business_id (str): The name of the business id column if it needs to be included.
            name (str): The name of the business name column if it needs to be included.
            data_points (list): List of data point keys that need to be included.

        Returns:
            The DataFrame.

        """
        data = [entry.to_list(business_id, name, data_points) for entry in entries]

        columns = []
        if business_id:
            columns.append(business_id)
        if name:
            columns.append(name)
        columns += data_points

        return pd.DataFrame(data, columns=columns)

    @classmethod
    def scrape_entries(cls, year):
        """Scrape entries from a given year.

        It will scrape the entries from the institutions on a given year.
        It will also index the non-standardized documents belonging to the entries.

        Args:
            year (int): The year to scrape

        """
        page = OverviewPage(year)
        scraper = EntryScraper(page)
        scraper.scrape_entries()
        n_results = scraper.save_results()
        print('{} entries and {} documents added to database'.format(*n_results))

    @classmethod
    def index_standardized_documents(cls, entries):
        """Index standardized documents belonging to the given entries.

        Args:
            entries (list): List of Entry objects.

        """
        n_documents = 0

        for entry in entries:
            page = DocumentsPage(entry)
            doc_scraper = DocumentScraper(page)
            doc_scraper.scrape_documents()
            n_documents += doc_scraper.save_results()

        print('{} documents added to database'.format(n_documents))

    @classmethod
    def download_documents(cls, entries):
        """Download documents needed for data extracting belonging to certain entries.

        The method for downloading documents can be found in the DocumentDownloader class.

        Args:
            entries (list): List of Entry objects.

        """
        necessary_documents = []
        for entry in entries:
            necessary_documents += entry.get_necessary_documents()
        downloader = DocumentDownloader(necessary_documents)
        downloader.download()

    @classmethod
    def extract_data(cls, entries, index_file):
        """Extract data from the documents belonging to the entries.

        It assumes the documents have been downloaded or they will be skipped.

        Args:
            entries (list): List of Entry objects.
            index_file (str): Path of the financial index file.
                The index file is needed to match the item names
                of the financial details to the given indexes.

        """
        cls.extract_financial_data(entries, index_file)
        cls.extract_entity_data(entries)
        cls.extract_employee_data(entries)

    @staticmethod
    def create_index_file(index_file, limit=10):
        """Create an index file for the financial details item names.

        It is created by selecting random financial documents and
        extracting the item names used in those files.

        Args:
            index_file (str): Path of the desired location for the index file.
            limit (int): The limit of the random number of documents chosen.

        """
        entries = db.session.query(Entry).order_by(func.random()).limit(limit)
        financial_documents = [entry.get_financial_document() for entry in entries]
        financial_documents = [doc for doc in financial_documents if doc is not None]
        FinanceDataExtractor.create_index_file(financial_documents, index_file)

    @classmethod
    def extract_financial_data(cls, entries, index_file):
        """Extract data from the financial documents belonging to the entries.

        The method for extracting financial data can be found in the FinanceDataExtractor class.

        Args:
            entries (list): List of Entry objects.
            index_file (str): Path of the financial index file.
                The index file is needed to match the item names
                of the financial details to the given indexes.

        """
        cls.extract_financial_data(entries, index_file)
        cls.extract_entity_data(entries)
        cls.extract_employee_data(entries)
        financial_documents = [entry.get_financial_document() for entry in entries]
        for doc in financial_documents:
            if doc and not doc.is_processed:
                print('Processing financial document for {}'.format(doc.entry.name))
                extractor = FinanceDataExtractor(doc, index_file=index_file)
                if extractor.pdf:
                    extractor.run()
                    extractor.save_results()

    @classmethod
    def extract_entity_data(cls, entries):
        """Extract data from the entity documents belonging to the entries.

        The method for extracting financial data can be found in the EntityDataExtractor class.

        Args:
            entries (list): List of Entry objects.

        """
        entity_documents = [entry.get_entity_document() for entry in entries]
        for doc in entity_documents:
            if doc and not doc.is_processed:
                print('Processing entity document for {}'.format(doc.entry.name))
                extractor = EntityDataExtractor(doc)
                if extractor.pdf:
                    extractor.run()
                    extractor.save_results()

    @classmethod
    def extract_employee_data(cls, entries):
        """Extract data from the employee documents belonging to the entries.

        The method for extracting financial data can be found in the EmployeeDataExtractor class.
        Currently only works reliably for employee documents from 2018.

        Args:
            entries (list): List of Entry objects.

        """
        employee_documents = [entry.get_employee_document() for entry in entries]
        for doc in employee_documents:
            if doc:
                print('Processing employee document for {}'.format(doc.entry.name))
                extractor = EmployeeDataExtractor(doc)
                if extractor.pdf:
                    extractor.run()
                    extractor.save_result()
