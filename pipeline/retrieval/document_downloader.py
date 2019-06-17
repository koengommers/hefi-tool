import os
import time
from itertools import groupby

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pipeline.retrieval.documents_page import DocumentsPage
from pipeline.retrieval.overview_page import OverviewPage


class DocumentDownloader:
    def __init__(self, documents, download_dir='data/temp', document_dir='data/pdf'):
        self.documents = documents
        self.download_dir = os.path.abspath(download_dir)
        self.document_dir = os.path.abspath(document_dir)

        self.standardized = []
        self.non_standardized = []
        self.split_documents()

    def split_documents(self):
        for doc in self.documents:
            if doc.standardized and not doc.downloaded:
                self.standardized.append(doc)
            elif not doc.downloaded:
                self.non_standardized.append(doc)

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "plugins.plugins_list": [{
                "enabled": False,
                "name": "Chrome PDF Viewer"
            }],
            "download": {
                "prompt_for_download": False,
                "default_directory": self.download_dir
            }
        })
        self.driver = webdriver.Chrome(options=chrome_options)

    def download(self):
        if self.standardized or self.non_standardized:
            self.init_driver()
            self.download_standardized()
            self.download_non_standardized()
            self.driver.quit()

    def download_standardized(self):
        entry_groups = [list(group) for entry_id, group in groupby(self.standardized, lambda doc: doc.entry_id)]
        entry_groups = [(group[0].entry, group) for group in entry_groups]
        for entry, docs in entry_groups:
            page = DocumentsPage(entry)
            self.driver.get(page.url)
            for doc in docs:
                if len(os.listdir(self.download_dir)) > 0:
                    raise RuntimeError('{} directory not clean'.format(self.download_dir))
                elem = self.driver.find_element_by_xpath('//a[@class="DocumentReportItem" and text() = "{}"]'.format(doc.label))
                elem.click()

                time.sleep(0.1)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                if self.driver.title == 'Fout pagina':
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                else:
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    while not [f for f in os.listdir(self.download_dir) if f.endswith('.pdf')]:
                        time.sleep(0.1)
                    filename = next(f for f in os.listdir(self.download_dir) if f.endswith('.pdf'))
                    os.rename(os.path.join(self.download_dir, filename), os.path.join(self.document_dir, doc.filename()))
                    doc.set_downloaded()

    def download_non_standardized(self):
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
