"""Contains DocumentDownloader class."""

import os
import time
from itertools import groupby

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException

from .documents_page import DocumentsPage
from .overview_page import OverviewPage


class DocumentDownloader:
    """Downloads documents efficiently.

    It will split the documents into non-standardized and standardized documents,
    because they have to be downloaded differently. Afterwards documents that
    are on the same page will be grouped, to avoiding having to load pages double.
    Documents are downloaded using a WebDriver. As the status of downloads cannot
    be read, it will download the documents to a temporarily directory, when a file
    is detected in that directory it will be renamed and moved.

    """

    def __init__(self, documents, download_dir='data/temp', document_dir='data/pdf'):
        """Init downloader object.

        It will split the documents into non-standardized and standardized documents,
        because they have to be downloaded differently.

        Args:
            documents (list): List of document objects to download.
            download_dir (str): Path to directory that temporarily stores downloads.
            document_dir (str): Path to directory that stores the documents.

        """
        self.documents = documents
        self.download_dir = os.path.abspath(download_dir)
        self.document_dir = os.path.abspath(document_dir)
        self.split_documents()

    def split_documents(self):
        """Split documents in non-standardized and standardized."""
        self.standardized = []
        self.non_standardized = []
        for doc in self.documents:
            if doc:
                if doc.standardized and not doc.downloaded:
                    self.standardized.append(doc)
                elif not doc.downloaded:
                    self.non_standardized.append(doc)

    def init_driver(self):
        """Start the WebDriver."""
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "plugins.plugins_list": [{
                "enabled": False,
                "name": "Chrome PDF Viewer"
            }],
            "plugins.always_open_pdf_externally": True,
            "download": {
                "prompt_for_download": False,
                "default_directory": self.download_dir
            }
        })
        self.driver = webdriver.Chrome(options=chrome_options)

    def download(self):
        """Start downloading the documents."""
        if self.standardized or self.non_standardized:
            self.init_driver()
            self.download_standardized()
            self.download_non_standardized()
            self.driver.quit()

    def check_directory(self):
        """Check if temporary download directory is empty."""
        if len(os.listdir(self.download_dir)) > 0:
            print('{} directory not empty'.format(self.download_dir))
            clear_directory = input('Want to remove its contents? [y/n] ') == 'y'
            if clear_directory:
                for file in os.listdir(self.download_dir):
                    filepath = os.path.join(self.download_dir, file)
                    if os.path.isfile(filepath):
                        os.unlink(filepath)
            else:
                exit()

    def download_standardized(self):
        """Download the standardized documents.

        Groups documents by entry (year and institution) because their links
        are on the same page.

        """
        entry_groups = [list(group) for entry_id, group in groupby(self.standardized, lambda doc: doc.entry_id)]
        entry_groups = [(group[0].entry, group) for group in entry_groups]
        for entry, docs in entry_groups:
            page = DocumentsPage(entry)
            self.driver.get(page.url)
            for doc in docs:
                self.check_directory()
                try:
                    elem = self.driver.find_element_by_xpath('//a[@class="DocumentReportItem" and text() = "{}"]'.format(doc.label))
                    elem.click()

                    time.sleep(0.1)
                    try:
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        if self.driver.title == 'Fout pagina':
                            print('Document #{} can\'t be downloaded'.format(doc.id))
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])
                            continue
                    except:
                        pass
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    while not [f for f in os.listdir(self.download_dir) if f.endswith('.pdf')]:
                        time.sleep(0.1)
                    filename = next(f for f in os.listdir(self.download_dir) if f.endswith('.pdf'))
                    os.rename(os.path.join(self.download_dir, filename), os.path.join(self.document_dir, doc.filename()))
                    doc.set_downloaded()
                except NoSuchElementException:
                    print('Document #{} can\'t be downloaded'.format(doc.id))

    def download_non_standardized(self):
        """Download the non-standardized documents.

        Groups documents by year because their links are on the same pages.

        """
        year_groups = [(year, list(group)) for year, group in groupby(self.non_standardized, lambda doc: doc.entry.year)]
        for year, docs in year_groups:
            page = OverviewPage(year, driver=self.driver)
            page.navigate_to_page()
            for doc in docs:
                page.download_document(doc)
                filename = doc.name + '.pdf'
                while filename not in os.listdir(self.download_dir):
                    time.sleep(0.1)
                os.rename(os.path.join(self.download_dir, filename), os.path.join(self.document_dir, doc.filename()))
                doc.set_downloaded()
