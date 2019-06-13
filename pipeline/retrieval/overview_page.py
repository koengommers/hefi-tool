import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select


class OverviewPage:
    def __init__(self, year, reload=False, driver=None):
        self.year = year
        self.html = None
        self.url = 'https://www.desan.nl/net/DoSearch/Search.aspx'
        self.driver = driver

        if not reload and os.path.isfile(self.html_file()):
            with open(self.html_file(), 'r') as file:
                self.html = file.read()

    def html_file(self):
        return 'data/html/overview-{}.html'.format(self.year)

    def init_driver(self):
        self.driver = webdriver.Chrome()

    def navigate_to_page(self):
        if not self.driver:
            self.init_driver()

        self.driver.get(self.url)
        select = Select(self.driver.find_element_by_name('zoeken_jaar'))
        if not str(self.year) in [option.text for option in select.options]:
            raise ValueError('Year not valid.')
        select.select_by_visible_text(str(self.year))

        search_button = self.driver.find_element_by_name('zoeken')
        search_button.click()

        if self.driver.title == 'Runtime Error':
            raise RuntimeError

    def download_document(self, document):
        entry_elem = self.driver.find_element_by_xpath('//table[@class="ct" and contains(.//th[@class="crth"]/text(), "{}")]'.format(document.entry.name))
        doc_elem = entry_elem.find_element_by_xpath("//a[normalize-space(text()) = '{}']".format(document.name))
        doc_elem.click()

    def download(self):
        self.navigate_to_page()
        self.html = self.driver.page_source
        self.save()

    def save(self):
        with open(self.html_file(), 'w') as file:
            file.write(self.html)

    def get_html(self):
        if not self.html:
            self.download()

        return self.html
