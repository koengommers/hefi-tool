"""Contains DocumentScraper class."""

from bs4 import BeautifulSoup

from ..database import db
from ..models import Document


class DocumentScraper:
    """Scrapes standardized documents pages.

    Indexes standardized documents on the standardized documents page
    of an entry. For every document it stores what entry it belongs to
    and the label of the document.

    """

    def __init__(self, page):
        """Init DocumentScraper object.

        Args:
            page (DocumentsPage): The page to scrape the documents from.

        """
        self.page = page
        self.soup = BeautifulSoup(page.get_html(), features='html.parser')
        self.documents = []

    def scrape_documents(self):
        """Start scraping for the documents."""
        doc_elems = self.soup.find_all('a', attrs={'class': 'DocumentReportItem'})
        if doc_elems:
            doc_elems = doc_elems[:-1]
            for elem in doc_elems:
                label = elem.get_text().strip()
                document = db.session.query(Document).filter_by(entry=self.page.entry, label=label).first()
                if not document:
                    document = Document(self.page.entry, label, True)
                    self.documents.append(document)

    def save_results(self):
        """Save the scraping results.

        Returns:
            (int) Number of documents found and indexed.

        """
        for doc in self.documents:
            db.session.add(doc)
        db.session.commit()
        return len(self.documents)
