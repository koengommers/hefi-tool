from sqlalchemy import func

from core.database import db
from models import Entry
from pipeline.processing.finance_data_extractor import FinanceDataExtractor
from pipeline.retrieval.document_downloader import DocumentDownloader
from pipeline.retrieval.document_scraper import DocumentScraper
from pipeline.retrieval.documents_page import DocumentsPage
from pipeline.retrieval.entry_scraper import EntryScraper
from pipeline.retrieval.overview_page import OverviewPage


class Pipeline:
    @classmethod
    def process_year(cls, year, index_file):
        cls.scrape_entries(year)

        entries = db.session.query(Entry).filter_by(year=year).all()
        cls.index_standardized_documents(entries)
        cls.download_documents(entries)
        cls.extract_data(entries, index_file)

    @classmethod
    def scrape_entries(cls, year):
        page = OverviewPage(year)
        scraper = EntryScraper(page)
        scraper.scrape_entries()
        n_results = scraper.save_results()
        print('{} entries and {} documents added to database'.format(*n_results))

    @classmethod
    def index_standardized_documents(cls, entries):
        n_documents = 0

        for entry in entries:
            page = DocumentsPage(entry)
            doc_scraper = DocumentScraper(page)
            doc_scraper.scrape_documents()
            n_documents += doc_scraper.save_results()

        print('{} documents added to database'.format(n_documents))

    @classmethod
    def download_documents(cls, entries):
        necessary_documents = []
        for entry in entries:
            necessary_documents += entry.get_necessary_documents()
        downloader = DocumentDownloader(necessary_documents)
        downloader.download()

    @classmethod
    def extract_data(cls, entries, index_file):
        cls.extract_financial_data(entries, index_file)

    @staticmethod
    def create_index_file(index_file, limit=10):
        entries = db.session.query(Entry).order_by(func.random()).limit(limit)
        financial_documents = [entry.get_financial_document() for entry in entries]
        financial_documents = [doc for doc in financial_documents if doc is not None]
        FinanceDataExtractor.create_index_file(financial_documents, index_file)

    @classmethod
    def extract_financial_data(cls, entries, index_file):
        financial_documents = [entry.get_financial_document() for entry in entries]
        for doc in financial_documents:
            if doc and not doc.is_processed:
                print('Processing financial document for {}'.format(doc.entry.name))
                extractor = FinanceDataExtractor(doc, index_file=index_file)
                extractor.run()
                extractor.save_results()
