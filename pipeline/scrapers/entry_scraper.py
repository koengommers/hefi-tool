import locale
import urllib.parse as urlparse
from datetime import datetime

from bs4 import BeautifulSoup

from core.database import db
from models import Document, Entry


class EntryScraper:
    def __init__(self, page):
        self.page = page
        self.year = page.year
        self.soup = BeautifulSoup(page.get_html(), features='html.parser')
        self.entries = []
        self.documents = []

    def scrape_entries(self):
        overview = self.soup.find('div', attrs={'id': 'resultaten'})
        if overview:
            for elem in overview.find_all('table', attrs={'class': 'ct'}):
                self.scrape_entry(elem)

    def scrape_entry(self, elem):
        name     = elem.find('th', attrs={'class': 'crth'}).get_text().strip()
        location = elem.find('th', attrs={'class': 'crthc2'}).get_text().strip()
        url      = elem.find('a', attrs={'class': 'digilink'}).get('href')

        parsed_url = urlparse.urlparse(url)
        business_id = urlparse.parse_qs(parsed_url.query)['kvkNumber'][0]

        entry = db.session.query(Entry).filter_by(business_id=business_id, year=self.year).first()
        if not entry:
            entry = Entry(business_id, self.year, name, location)
            self.entries.append(entry)
            self.scrape_documents(entry, elem)

    def scrape_documents(self, entry, entry_elem):
        for elem in entry_elem.find_all('table', attrs={'class': 'filerowcons'}):
            name_column = elem.find('td', text='naam')
            link = name_column.find_next('td').find('a')
            name = link.get_text().strip()
            url = urlparse.urljoin(self.page.url, link.get('href'))

            label_column = elem.find('td', text='inhoud')
            label = label_column.find_next('td').get_text().strip()

            published_text = elem.find_all('tr')[-1].get_text().strip().replace('gepubliceerd op ', '')
            locale.setlocale(locale.LC_TIME, 'nl_NL')
            published_on = datetime.strptime(published_text, '%A %d %B %Y').date()

            document = Document(entry, label, False, name, published_on, url)
            self.documents.append(document)

    def save_results(self):
        for obj in self.entries + self.documents:
            db.session.add(obj)
        db.session.commit()
        return len(self.entries), len(self.documents)
