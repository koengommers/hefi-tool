"""Contains OverviewPage class."""

import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select


class OverviewPage:
    """Represents the overview page of a year."""

    def __init__(self, year, reload=False, driver=None):
        """Init the class.

        Args:
            year (int): The year to get the overview page for.
            reload (bool): Whether to reload the page if it is already downloaded.
            driver (selenium.webdriver.Chrome): The web driver to be used.
                If none is given than a new webdriver will be started.

        """
        self.year = year
        self.html = None
        self.url = 'https://www.desan.nl/net/DoSearch/Search.aspx'
        self.driver = driver

        if not reload and os.path.isfile(self.html_file()):
            with open(self.html_file(), 'r') as file:
                self.html = file.read()

    def html_file(self):
        """Get HTML file path for saving the document.

        Returns:
            (str) Path for the HTML file.

        """
        return 'data/html/overview-{}.html'.format(self.year)

    def init_driver(self):
        """Start a new webdriver."""
        self.driver = webdriver.Chrome()

    def navigate_to_page(self):
        """Let the webdriver navigate to the page."""
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
        """Download a document that is on the page.

        Args:
            document (Document): The document to download.

        """
        entry_elem = self.driver.find_element_by_xpath('//table[@class="ct" and contains(.//th[@class="crth"]/text(), "{}")]'.format(document.entry.name))
        doc_elem = entry_elem.find_element_by_xpath("//a[normalize-space(text()) = '{}']".format(document.name))
        doc_elem.click()

    def download(self):
        """Get the HTML content from the URL."""
        self.navigate_to_page()
        self.html = self.driver.page_source
        self.save()

    def save(self):
        """Save the HTML for caching purposes.

        The HTML file is saved because the website sometimes has
        outages, in that case the saved file can be used.

        """
        with open(self.html_file(), 'w') as file:
            file.write(self.html)

    def get_html(self):
        """Get HTML for the page.

        Downloads the HTML if it doesn't have it yet.

        Returns:
            (str) HTML content.

        """
        if not self.html:
            self.download()

        return self.html
