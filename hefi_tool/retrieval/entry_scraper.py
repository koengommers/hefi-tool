"""Contains EntryScraper class."""

import locale
import urllib.parse as urlparse
from datetime import datetime

from bs4 import BeautifulSoup

from ..database import db
from ..models import Document, Entry, Year


class EntryScraper:
    """Scrapes overview page for entries.

    Scrapes the listings page of a year for the institution information on it.
    It also indexes the non-standardized documents on the page. For every
    institution it saves the business id (KvK nummer), the name and the
    location of the institution and the year.

    """

    def __init__(self, page):
        """Init the class.

        Args:
            page (OverviewPage): The page to scrape.

        """
        self.page = page
        self.year = page.year
        self.soup = BeautifulSoup(page.get_html(), features='html.parser')
        self.entries = []
        self.documents = []
        self.year_exists = bool(db.session.query(Year).filter_by(year=self.year).first())

    def scrape_entries(self):
        """Start scraping the page for entries."""
        overview = self.soup.find('div', attrs={'id': 'resultaten'})
        if overview:
            for elem in overview.find_all('table', attrs={'class': 'ct'}):
                self.scrape_entry(elem)

    def scrape_entry(self, elem):
        """Get data from an element containing an entry.

        Args:
            elem: BeautifulSoup element that contains the entry.

        """
        name     = elem.find('th', attrs={'class': 'crth'}).get_text().strip()
        location = elem.find('th', attrs={'class': 'crthc2'}).get_text().strip()
        url      = elem.find('a', attrs={'class': 'digilink'}).get('href')

        parsed_url = urlparse.urlparse(url)
        business_id = urlparse.parse_qs(parsed_url.query)['kvkNumber'][0]

        if not self.year_exists:
            digimv_url = url.replace(business_id, '')
            year_obj = Year(self.year, digimv_url)
            db.session.add(year_obj)
            db.session.commit()
            self.year_exists = True

        entry = db.session.query(Entry).filter_by(business_id=business_id, year=self.year).first()
        if not entry:
            entry = Entry(business_id, self.year, name, location)
            self.entries.append(entry)
            self.scrape_documents(entry, elem)

    def scrape_documents(self, entry, entry_elem):
        """Scrape non-standardized documents belonging to an entry.

        Args:
            entry (Entry): The entry to scrape the documents for.
            entry_elem: The BeautifulSoup element that contains the data.

        """
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
        """Save the scraping results.

        Returns:
            (tuple) Number of entries and number of documents scraped.

        """
        for obj in self.entries + self.documents:
            db.session.add(obj)
        db.session.commit()
        return len(self.entries), len(self.documents)
