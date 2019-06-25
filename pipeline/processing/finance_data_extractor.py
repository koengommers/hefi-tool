import pdfquery
import re
from jellyfish import jaro_winkler
from pdfminer.layout import LTTextLineHorizontal
from pdfminer.layout import LTPage


class FinanceDataExtractor:

    def __init__(self, document, index_file=None):
        self.document = document
        self.index_file = index_file
        path = document.get_path(download=False)
        if path:
            try:
                self.pdf = pdfquery.PDFQuery(path)
                self.get_columns()
            except:
                self.pdf = None
        else:
            self.pdf = None

    @staticmethod
    def normalize_index(index):
        """Returns a normalized index"""
        index = index.lower()
        index = index.replace('som der', 'totaal')
        return re.sub(' \(.*\)?', '', index)

    @classmethod
    def create_index_file(cls, documents, return_file):
        """Input is a list of finance file paths which indexes are used."""
        total_keys = []
        for doc in documents:
            extractor = cls(doc)
            extractor.build_query()
            results = extractor.pdf.extract(extractor.query, as_dict=False)
            keys = [key[-1] for key in results[::3]]
            if total_keys:
                for key in keys:
                    scores = [jaro_winkler(cls.normalize_index(key), cls.normalize_index(x)) for x in total_keys]
                    jaro_best = max(scores)
                    match = total_keys[scores.index(jaro_best)]
                    if jaro_best <= 0.86:
                        total_keys.append(cls.normalize_index(key))
            else:
                total_keys.extend([cls.normalize_index(key) for key in keys])

        with open(return_file, 'w') as rfile:
            for key in total_keys:
                rfile.write(key + '\n')

    @staticmethod
    def bbox_to_string(bbox):
        return ', '.join(map(str, bbox))

    @staticmethod
    def bbox_to_list(bbox):
        return bbox.strip('[]').split(', ')

    def is_in_right_column(self, obj, max_edge_distance=10):
        """
        This function returns whether an object is in the right column.
        """
        [x1,y1,x2,y2] = obj.get('bbox').strip('[]').split(', ')
        return obj.text and abs(float(x2) - float(self.right_column_x[1])) < max_edge_distance

    def get_columns(self):
        """
        This function stores the coordinates of the middle and right column.
        """
        column_bboxes = self.pdf.extract([
            ('with_formatter', lambda results: results[0].get('bbox').strip('[]').split(', ')),
            (0, 'LTTextLineHorizontal:contains("Bedrag in euro\'s per einde verslagjaar")'),
            (1, 'LTTextLineHorizontal:contains("Bedrag in euro\'s per einde vorig")')
        ], as_dict=False)
        self.left_column_x = (column_bboxes[0][1][0], column_bboxes[0][1][2])
        self.right_column_x = (column_bboxes[1][1][0], column_bboxes[1][1][2])

    def get_value_locations(self):
        """
        This function takes the objects in the right column,
        returns list with bounding boxes of values in all columns.
        """
        right_column_objects = list(filter(self.is_in_right_column, self.pdf.pq('LTTextBoxHorizontal:contains("euro")')))
        value_locations = []
        left_col_x1, left_col_x2 = self.left_column_x
        index_x1, index_x2 = 50, 220
        for obj in right_column_objects:
            page_index = next(obj.iterancestors('LTPage')).get('page_index', 0)
            obj_bbox = self.bbox_to_list(obj.get('bbox'))
            index_bbox = self.bbox_to_string([index_x1, obj_bbox[1], index_x2, obj_bbox[3]])
            this_year = self.bbox_to_string([left_col_x1, obj_bbox[1], left_col_x2, obj_bbox[3]])
            last_year = obj.get('bbox').strip('[]')
            value_locations.append((page_index, index_bbox, this_year, last_year))
        return value_locations

    def build_query(self):
        """
        This function takes the bounding boxes,
        returns a query to extract all values.
        """
        value_locations = self.get_value_locations()
        self.query = [('with_formatter', 'text')]
        for i, locations in enumerate(value_locations):
            page_index, index_bbox, this_year_bbox, last_year_bbox = locations
            self.query.append(('with_parent','LTPage[page_index="{}"]'.format(page_index)))
            self.query.append((i, 'LTTextLineHorizontal:overlaps_bbox("{}")'.format(index_bbox)))
            self.query.append((i, 'LTTextBoxHorizontal:overlaps_bbox("{}")'.format(this_year_bbox)))
            self.query.append((i, 'LTTextBoxHorizontal:overlaps_bbox("{}")'.format(last_year_bbox)))

    def match_index(self, index):
        """
        Input is an index from the finance document,
        Output is the matched index from the file.
        """
        with open(self.index_file, 'r', encoding='utf-8') as f:
            file_indexes = [x.strip('\n').lower() for x in f]
        jaro_score = [jaro_winkler(self.normalize_index(index), self.normalize_index(x)) for x in file_indexes]
        jaro_best = max(jaro_score)
        match = file_indexes[jaro_score.index(jaro_best)]
        if jaro_best <= 0.86:
            return self.normalize_index(index)
        else:
            return match

    @staticmethod
    def get_numerical(value):
        """Takes a string value and returns a numerical value"""
        value = value.replace('.', '')
        match = re.search('-?[0-9]+', value)
        if match is not None:
            return int(match.group(0))
        return None

    def to_dict(self, results):
        """
        This function takes a list of the query results,
        returns a dict for each year.
        """
        this_year, last_year = dict(), dict()
        i = 0
        while i <= len(results[:-3]):
            index = self.match_index(results[i][-1])
            this_year[index] = self.get_numerical(results[i+1][-1])
            last_year[index] = self.get_numerical(results[i+2][-1])
            i += 3
        return this_year, last_year

    def get_results(self):
        results = self.pdf.extract(self.query, as_dict=False)
        self.results = self.to_dict(results)
        return self.results

    def save_results(self):
        entry = self.document.entry
        this_year, last_year = self.results
        for index, value in this_year.items():
            entry.add_data_point(index, value)
        for index, value in last_year.items():
            entry.add_data_point('Voorgaand jaar: {}'.format(index), value)
        self.document.set_processed()

    def run(self):
        """
        Run all the query, return results in a dict for each year.
        """
        self.build_query()
        return self.get_results()
