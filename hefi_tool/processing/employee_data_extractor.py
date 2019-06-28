"""Contains EmployeeDataExtractor class."""

import re

import pdfquery
from jellyfish import jaro_winkler

from ..database import db
from ..models import Document


class EmployeeDataExtractor:
    """Extracts data about amount of employees.

    Employee documents differ from year to year. The used method assumes a document from
    2018 is used. It extracts the total amount of employees at the end of the year.

    """

    def __init__(self, document):
        """Begin a new data extraction.

        Args:
            document (Document): An employee document.

        """
        self.document = document
        self.column = None
        path = document.get_path(download=False)
        if path:
            try:
                self.pdf = pdfquery.PDFQuery(path)
            except:
                self.pdf = None
        else:
            self.pdf = None

    @staticmethod
    def get_bbox(elem):
        """Get list of coordinates of the bounding box from an element.

        Args:
            elem: The element to get the bbox for.

        Returns:
            (list) Coordinates of the bounding box.

        """
        if len(elem) > 0:
            return elem[0].get('bbox').strip('[]').split(', ')
        return None

    def locate_column(self):
        """Locate the column containing number employees end of year."""
        result = self.pdf.extract([
            ('with_formatter', lambda results: self.get_bbox(results)),
            ('totaal personeel', 'LTTextBoxHorizontal:contains("Personeel per einde verslagjaar")')
        ])
        if result['totaal personeel'] is not None:
            self.column = [float(x) for x in result['totaal personeel']]

    @staticmethod
    def get_numerical(value):
        """Get a numerical value out of a string.

        Args:
            value (str): The string containing a possible numeric value.

        Returns:
            (int) The found numeric value.

        """
        value = value.replace('.', '')
        match = re.search('[0-9]+', value)
        if match is not None:
            return int(match.group(0))
        return None

    def get_employees(self):
        """Extract number of total employees at end of the year.

        Returns:
            (dict) Dictionary of results.

        """
        bbox = self.column
        if bbox is not None:
            new_bbox = str([sum(x) for x in zip(bbox, [180, -125, 180, -125])]).strip('[]')
            self.result = self.pdf.extract([
                ('with_formatter', lambda results: self.get_numerical(results.text())),
                ('totaal personeel', 'LTTextLineHorizontal:overlaps_bbox("{}")'.format(new_bbox))
            ])
            return self.result
        else:
            self.result = {'totaal personeel' : None}
        return self.result

    def run(self):
        """Run the extraction."""
        self.locate_column()
        self.get_employees()

    def save_result(self):
        """Save the result."""
        entry = self.document.entry
        for index, value in self.result.items():
            entry.add_data_point(index, value)
        self.document.set_processed()
