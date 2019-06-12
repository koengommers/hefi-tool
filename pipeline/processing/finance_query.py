import pdfquery
import re
from pdfminer.layout import LTTextLineHorizontal
from pdfminer.layout import LTPage
from pdfminer.layout import LTChar


class FinanceDocument(object):

    def __init__(self, path, data):
        self.path = path
        self.data = data
        self.pdf = pdfquery.PDFQuery(path)

    def build_q(self):
        """
        Build a query for extracting indexes.
        """
        return [(index, 'LTTextLineHorizontal:contains("' + index + '")') for index in self.data]

    def choose(self, res):
        """
        Choose indexes with a bounding box of certain heigth.
        This way no titles are chosen.
        """
        for r in res:
            if float(r.get('height', 0)) < 8.2:
                return r
        return None

    def get_cols(self):
        """
        Get coordinates of the two columns in a financial document.
        """
        result = self.pdf.extract([
            ('with_parent', 'LTPage[page_index="1"]'),
            ('column 1', 'LTTextLineHorizontal:contains("Bedrag in euro\'s per einde verslagjaar")'),
            ('column 2', 'LTTextLineHorizontal:contains("Bedrag in euro\'s per einde vorig")')
        ])
        coords = []
        for res in result.values():
            coords.append([float(x) for x in res[0].get('bbox').strip('[]').split(', ')])
        return coords

    def get_good(self, result):
        """
        When multiple results of certain index choose the first occurring.
        """
        new = dict()
        for index, res in result.items():
           new[index] = self.choose(res)
        return new

    def get_bboxes(self, result, cols):
        """
        Get bounding boxes of values of indexes in retrieved columns.
        """
        new = dict()
        for index, res in result.items():
            if res is None:
                new[index] = None
            else:
                page_index = next(res.iterancestors('LTPage')).get('page_index', 0)
                x, y, x2, y2 = [float(x) for x in res.get('bbox').strip('[]').split(', ')]
                new[index] = ([cols[0][0], y, cols[0][2], y2], [cols[1][0], y, cols[1][2], y2], page_index)
        return new

    def build_col_q(self, bboxes):
        """
        Build the query for retrieving all the values of indexes.
        """
        col_q1 = [('with_formatter', 'text')]
        col_q2 = [('with_formatter', 'text')]
        for index, coord in bboxes.items():
            if coord is not None:
                page_id = coord[2]
                coord_1 = ', '.join(map(str, coord[0]))
                coord_2 = ', '.join(map(str, coord[1]))
            else:
                page_id = '0'
                coord_1 = coord_2 = '0, 0, 0, 0'
            col_q1.append(('with_parent','LTPage[page_index="{}"]'.format(page_id)))
            col_q2.append(('with_parent','LTPage[page_index="{}"]'.format(page_id)))
            col_q1.append((index, 'LTTextLineHorizontal:overlaps_bbox("{}")'.format(coord_1)))
            col_q2.append((index, 'LTTextLineHorizontal:overlaps_bbox("{}")'.format(coord_2)))
        return col_q1, col_q2

    def query(self, q):
        """
        Run all the queries.
        """
        result = self.get_good(self.pdf.extract(q))
        cols = self.get_cols()
        bboxes = self.get_bboxes(result, cols)
        col_q1, col_q2 = self.build_col_q(bboxes)
        one = self.pdf.extract(col_q1)
        two = self.pdf.extract(col_q2)
        return one, two
