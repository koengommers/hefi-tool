import pdfquery
import re
from jellyfish import jaro_winkler
from core.database import db
from models import Document

class EmployeeDataExtractor:

    def __init__(self, document):
        self.document = document
        self.pdf = pdfquery.PDFQuery(document.get_path())

    def locate_column(self):
        result = self.pdf.extract([
            ('with_formatter', lambda results: results[0].get('bbox').strip('[]').split(', ')),
            ('totaal personeel', 'LTTextBoxHorizontal:contains("Personeel per einde verslagjaar")')
        ])
        return [float(x) for x in result['totaal personeel']]

    @staticmethod
    def get_numerical(value):
        """Takes a string value and returns a numerical value"""
        value = value.replace('.', '')
        match = re.search('[0-9]+', value)
        if match is not None:
            return int(match.group(0))
        return None

    def get_employees(self, bbox):
        new_bbox = str([sum(x) for x in zip(bbox, [180, -125, 180, -125])]).strip('[]')
        self.result = self.pdf.extract([
            ('with_formatter', lambda results: self.get_numerical(results.text())),
            ('totaal personeel', 'LTTextLineHorizontal:overlaps_bbox("{}")'.format(new_bbox))
        ])
        return self.result

    def run(self):
        bbox = self.locate_column()
        self.get_employees(bbox)

    def save_result(self):
        entry = self.document.entry
        for index, value in self.result.items():
            entry.add_data_point(index, value)
        self.document.set_processed()
