import os
import urllib.parse as urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from core.database import db
from models import Entry


class OverviewScraper:
    def __init__(self, year, load=True):
        self.year = year
        self.html = None
        self.results = []

        if not load and os.path.isfile(self.html_file()):
            with open(self.html_file(), 'r') as file:
                self.html = file.read()

    def html_file(self):
        return 'data/html/overview-{}.html'.format(self.year)

    def save_html(self):
        with open(self.html_file(), 'w') as file:
            file.write(self.html)

    def scrape(self):
        if not self.html:
            self.get_html()

        soup = BeautifulSoup(self.html, features='html.parser')
        overview = soup.find('div', attrs={'id': 'resultaten'})
        if overview:
            self.save_html()
            for elem in overview.find_all('table', attrs={'class': 'ct'}):
                self.scrape_institution_data(elem)

    def scrape_institution_data(self, elem):
        name     = elem.find('th', attrs={'class': 'crth'}).get_text().strip()
        location = elem.find('th', attrs={'class': 'crthc2'}).get_text().strip()
        url      = elem.find('a', attrs={'class': 'digilink'}).get('href')

        parsed_url = urlparse.urlparse(url)
        business_id = urlparse.parse_qs(parsed_url.query)['kvkNumber'][0]

        entry = db.session.query(Entry).filter_by(business_id=business_id, year=self.year).first()
        if not entry:
            self.results.append(Entry(business_id, self.year, name, location))

    def get_html(self):
        driver = webdriver.Chrome()
        driver.get('https://www.desan.nl/net/DoSearch/Search.aspx')

        select = Select(driver.find_element_by_name('zoeken_jaar'))
        if not str(self.year) in [option.text for option in select.options]:
            raise ValueError('Year not valid.')
        select.select_by_visible_text(str(self.year))

        continue_button = driver.find_element_by_class_name('linkcontinue')
        continue_button.click()

        self.html = driver.page_source

    def save_results(self):
        db.session.bulk_save_objects(self.results)
        db.session.commit()
        return len(self.results)
