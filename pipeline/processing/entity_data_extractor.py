import pdfquery
import re

class EntityDataExtractor:

    def __init__(self, document):
        self.document = document
        path = document.get_path(download=False)
        if path:
            self.pdf = pdfquery.PDFQuery(path)
            self.pdf.load()
        else:
            self.pdf = None

    @staticmethod
    def above_y_split():
        return float(this.get('y1')) > 700

    @staticmethod
    def below_y_split():
        return float(this.get('y1')) < 700

    @staticmethod
    def filter_height():
        return float(this.get('height')) > 200

    def is_registered(self):
        """Returns whether the institution is registered at the Chamber of Commerce."""
        results = self.pdf.pq('LTCurve').filter(self.above_y_split)
        return float(results[1].get('height')) < 6

    def list_institution_types(self, result):
        """Returns a list of all the institution types"""
        entity_forms = []
        result = [elem for elem in result if elem.tag != 'LTImage']
        for elem in result:
            # Join any text that is in separate subelements and fix spaces.
            text = ''.join([subelem.text.replace('C ', 'C') for subelem in elem]).strip()
            # Remove text between parentheses.
            text = re.sub(' \(.*\)?', '', text)
            entity_forms.append(text)
        return entity_forms

    @staticmethod
    def option_is_checked(elem):
        return 'raw=134' in elem.get('stream')

    @staticmethod
    def bbox_to_string(bbox):
        return ', '.join(map(str, bbox))

    @staticmethod
    def bbox_to_list(bbox):
        return bbox.strip('[]').split(', ')

    def find_institution_type(self):
        """Returns the checked institution type"""

        container = self.pdf.pq('LTRect').filter(self.filter_height)
        if not container:
            return None

        container = container[0]
        entity_forms = self.list_institution_types(container)

        return [entity_forms[i] for i, elem in enumerate(container.findall('LTImage')) if self.option_is_checked(elem)]

    def find_legal_form(self):
        """Returns a string containing the checked legal form"""

        legal_forms = [
            'Publiekrechtelijke rechtspersoon',
            'Eenmanszaak',
            'Vennootschap onder firma (VoF)', 'Maatschap',
            'Commanditaire vennootschap (CV)',
            'Besloten vennootschap (BV) met Raad van Toezicht / Raad van Commissarissen',
            'Besloten vennootschap (BV) zonder Raad van Toezicht / Raad van Commissarissen',
            'Naamloze vennootschap (NV)',
            'Coöperatie en onderlinge waarborgmaatschappij',
            'Stichting',
            'Vereniging met volledige rechtsbevoegdheid',
            'Vereniging zonder volledige rechtsbevoegdheid',
            'Coöperatieve vereniging',
            'Kerkgenootschap',
            'andere rechtsvorm, namelijk:'
        ]

        options = self.pdf.pq('LTCurve').filter(self.below_y_split)

        legal_form = None
        for i, elem in enumerate(options):
            if float(elem.get('height')) < 6:
                # -1 because checked circle has 2 LTCurve elements
                legal_form = legal_forms[i - 1]
                break

        if legal_form == legal_forms[-1]:
            checked_bbox = map(float, self.bbox_to_list(elem.get('bbox')))
            other_legal_form_bbox = self.bbox_to_string(sum(x) for x in zip(checked_bbox, [0, -15, 0, -15]))
            other_legal_form = self.pdf.pq('LTPage[page_index="0"] LTTextLineHorizontal:overlaps_bbox("{}")'.format(other_legal_form_bbox))
            legal_form = 'anders: {}'.format(other_legal_form.text())

        return legal_form

    def run(self):
        self.results = {
            'registered': self.is_registered(),
            'legal form': self.find_legal_form(),
            'institution type': self.find_institution_type()
        }

    def save_results(self):
        entry = self.document.entry
        for key, value in self.results.items():
            entry.add_data_point(key, value)
        self.document.set_processed()
