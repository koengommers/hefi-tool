import urllib.parse as urlparse

from bs4 import BeautifulSoup

from core.database import db
from models import Entry


class EntryScraper:
    def __init__(self, page):
        self.year = page.year
        self.soup = BeautifulSoup(page.get_html(), features='html.parser')
        self.entries = []

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
            self.entries.append(Entry(business_id, self.year, name, location))

    def save_results(self):
        db.session.bulk_save_objects(self.entries)
        db.session.commit()
        return len(self.entries)
