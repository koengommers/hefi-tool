import pdfquery
import re
from jellyfish import jaro_winkler
from pdfminer.layout import LTTextLineHorizontal
from pdfminer.layout import LTPage


class FinanceDocument(object):

    def __init__(self, path):
        self.path = path
        self.pdf = pdfquery.PDFQuery(path)
        self.right_column = None
        self.left_column = None

    def filter_values(self, value):
        """
        This function returns whether an object is in the right column.
        """
        [x1,y1,x2,y2] = value.get('bbox').strip('[]').split(', ')
        return abs(float(x2) - float(self.right_column[2])) < 10 and len(value.text) > 0

    def get_columns(self):
        """
        This function stores the coordinates of the middle and right column.
        """
        result = self.pdf.extract([
            ('column 1', 'LTTextLineHorizontal:contains("Bedrag in euro\'s per einde verslagjaar")'),
            ('column 2', 'LTTextLineHorizontal:contains("Bedrag in euro\'s per einde vorig")')
        ])
        self.left_column = result['column 1'][0].get('bbox').strip('[]').split(', ')
        self.right_column = result['column 2'][0].get('bbox').strip('[]').split(', ')

    def get_right_column(self):
        """
        This function returns all values in the right column as a list.
        """
        self.get_columns()
        euros = list(filter(self.filter_values,
                            self.pdf.pq('LTTextBoxHorizontal:contains("euro")')))
        return euros

    def get_bboxes(self, right_column):
        """
        This function takes the objects in the right column,
        returns list with bounding boxes of values in all columns.
        """
        bboxes = []
        left_col_x1 = self.left_column[0]
        left_col_x2 = self.left_column[2]
        for right in right_column:
            page_index = next(right.iterancestors('LTPage')).get('page_index', 0)
            last_year = right.get('bbox').strip('[]').split(', ')
            this_year = ', '.join(map(str, [left_col_x1, last_year[1], left_col_x2, last_year[3]]))
            index_bbox = ', '.join(map(str,['50', last_year[1], '220', last_year[3]]))
            last_year = right.get('bbox').strip('[]')
            bboxes.append((page_index, str(index_bbox), str(this_year), last_year))
        return bboxes

    def build_query(self, bboxes):
        """
        This function takes the bounding boxes,
        returns a query to extract al values.
        """
        query = [('with_formatter', 'text')]
        for i,locations in enumerate(bboxes):
            page_id, index, this_year, last_year = locations
            query.append(('with_parent','LTPage[page_index="{}"]'.format(page_id)))
            query.append((i,'LTTextLineHorizontal:overlaps_bbox("{}")'.format(index)))
            query.append((i,'LTTextBoxHorizontal:overlaps_bbox("{}")'.format(this_year)))
            query.append((i,'LTTextBoxHorizontal:overlaps_bbox("{}")'.format(last_year)))
        return query

    def normalize(self, index):
        """Returns a normalized index"""
        index = index.lower()
        index = index.replace('som der', 'totaal')
        return re.sub('\(.*\)?','',index)

    def match_index(self, index, file):
        """
        Input is an index from the finance document,
        Output is the matched index from the file.
        """
        with open(file, 'r', encoding='utf-8') as f:
            file_indexes = [x.strip('\n').lower() for x in f]
        jaro_score = [jaro_winkler(self.normalize(index), self.normalize(x)) for x in file_indexes]
        jaro_best = max(jaro_score)
        match = file_indexes[jaro_score.index(jaro_best)]
        if jaro_best <= 0.86:
            return self.normalize(index)
        else:
            return match

    def get_numerical(self, value):
        """Takes a string value and returns a numerical value"""
        value = value.replace('.','')
        match = re.search('[0-9]+',value)
        if match is not None:
            return int(match.group(0))
        return None

    def nice_format(self, results):
        """
        This function takes a list of the query results,
        returns a dict for each year.
        """
        this_year, last_year = dict(), dict()
        i = 0
        while i <= len(results[:-3]):
            index = self.match_index(results[i][-1], 'indexes2.txt')
            this_year[index] = self.get_numerical(results[i+1][-1])
            last_year[index] = self.get_numerical(results[i+2][-1])
            i += 3
        return this_year, last_year

    def query(self):
        """
        Run all the query, return results in a dict for each year.
        """
        right_column = self.get_right_column()
        bboxes = self.get_bboxes(right_column)
        query = self.build_query(bboxes)
        results = self.pdf.extract(query, as_dict=False)
        return self.nice_format(results)
