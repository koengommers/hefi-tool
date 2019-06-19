import pdfquery
import re
from jellyfish import jaro_winkler
from core.database import db
from models import Document

class EmployeeDataExtractor:

    def __init__(self, document):
        self.document = document
        path = document.get_path(download=False)
        if path:
            self.pdf = pdfquery.PDFQuery(path)
        else:
            self.pdf = None

    @staticmethod
    def get_bbox(result):
        if len(result) > 0:
            return result[0].get('bbox').strip('[]').split(', ')
        return None

    def locate_column(self):
        result = self.pdf.extract([
            ('with_formatter', lambda results: self.get_bbox(results)),
            ('totaal personeel', 'LTTextBoxHorizontal:contains("Personeel per einde verslagjaar")')
        ])
        if result['totaal personeel'] is not None:
            return [float(x) for x in result['totaal personeel']]
        return None

    @staticmethod
    def get_numerical(value):
        """Takes a string value and returns a numerical value"""
        value = value.replace('.', '')
        match = re.search('[0-9]+', value)
        if match is not None:
            return int(match.group(0))
        return None

    def get_employees(self, bbox):
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
        bbox = self.locate_column()
        self.get_employees(bbox)

    def save_result(self):
        entry = self.document.entry
        for index, value in self.result.items():
            entry.add_data_point(index, value)
        self.document.set_processed()
