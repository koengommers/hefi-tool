from bs4 import BeautifulSoup

from core.database import db
from models import Document


class DocumentScraper:
    def __init__(self, page):
        self.page = page
        self.soup = BeautifulSoup(page.get_html(), features='html.parser')
        self.documents = []

    def scrape_documents(self):
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
        for doc in self.documents:
            db.session.add(doc)
        db.session.commit()
        return len(self.documents)
