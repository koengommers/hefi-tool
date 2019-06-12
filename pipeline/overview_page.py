import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select


class OverviewPage:
    def __init__(self, year, reload=False):
        self.year = year
        self.html = None
        self.url = 'https://www.desan.nl/net/DoSearch/Search.aspx'

        if not reload and os.path.isfile(self.html_file()):
            with open(self.html_file(), 'r') as file:
                self.html = file.read()

    def html_file(self):
        return 'data/html/overview-{}.html'.format(self.year)

    def download(self):
        driver = webdriver.Chrome()
        driver.get(self.url)

        select = Select(driver.find_element_by_name('zoeken_jaar'))
        if not str(self.year) in [option.text for option in select.options]:
            raise ValueError('Year not valid.')
        select.select_by_visible_text(str(self.year))

        continue_button = driver.find_element_by_class_name('linkcontinue')
        continue_button.click()

        if driver.title == 'Runtime Error':
            raise RuntimeError

        self.html = driver.page_source
        self.save()

    def save(self):
        with open(self.html_file(), 'w') as file:
            file.write(self.html)

    def get_html(self):
        if not self.html:
            self.download()

        return self.html
