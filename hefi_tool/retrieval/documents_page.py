"""Contains DocumentsPage class."""

import os
import requests


class DocumentsPage:
    """Represents a listings page of non-standardized documents."""

    def __init__(self, entry, reload=False):
        """Init the class.

        Args:
            entry (Entry): The entry to get the listings page from.
            reload (bool): Whether to reload the page if it is already downloaded.

        """
        self.html = None
        self.entry = entry
        self.url = entry.year_obj.digimv_url + entry.business_id

        if not reload and os.path.isfile(self.html_file()):
            with open(self.html_file(), 'r') as file:
                self.html = file.read()

    def html_file(self):
        """Get HTML file path for saving the document.

        Returns:
            (str) Path for the HTML file.

        """
        return 'data/html/documents-{}-{}.html'.format(self.entry.year, self.entry.business_id)

    def download(self):
        """Get the HTML content from the URL."""
        res = requests.get(self.url)
        res.raise_for_status()
        self.html = res.text
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
