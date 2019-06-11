import os
import requests


class DocumentsPage:
    def __init__(self, entry, reload=False):
        self.html = None
        self.entry = entry
        self.url = entry.year_obj.digimv_url + entry.business_id

        if not reload and os.path.isfile(self.html_file()):
            with open(self.html_file(), 'r') as file:
                self.html = file.read()

    def html_file(self):
        return 'data/html/documents-{}-{}.html'.format(self.entry.year, self.entry.business_id)

    def download(self):
        res = requests.get(self.url)
        res.raise_for_status()
        self.html = res.text
        self.save()

    def save(self):
        with open(self.html_file(), 'w') as file:
            file.write(self.html)

    def get_html(self):
        if not self.html:
            self.download()

        return self.html
