"""Contains EntityDataExtractor class."""

import pdfquery
import re

class EntityDataExtractor:
    """Extracts data about the institution entity.

    It extracts the legal form, whether the institution is registered
    at the Chamber of Commerce and the type of care they provide.

    """

    def __init__(self, document):
        """Begin a new data extraction.

        Args:
            document (Document): An entity document.

        """
        self.document = document
        path = document.get_path(download=False)
        if path:
            try:
                self.pdf = pdfquery.PDFQuery(path)
                self.pdf.load()
            except:
                self.pdf = None
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
        """Check whether the institution is registered at the Chamber of Commerce.

        Returns:
            (bool|None) A boolean if the result can be found, else None.

        """
        results = self.pdf.pq('LTCurve').filter(self.above_y_split)
        if results:
            return float(results[1].get('height')) < 6
        else:
            return None

    def list_institution_types(self, result):
        """Get a list of all the institution types on the document.

        Args:
            result: Element that contains the institution types.

        Returns:
            (list) List of institution types

        """
        entity_forms = []
        result = [elem for elem in result if elem.tag != 'LTImage']
        for elem in result:
            # Join any text that is in separate subelements and fix spaces.
            text = ''.join([subelem.text.replace('C ', 'C') for subelem in elem]).strip()
            # Remove text between parentheses.
            text = re.sub(r' \(.*\)?', '', text)
            entity_forms.append(text)
        return entity_forms

    @staticmethod
    def option_is_checked(elem):
        """Check whether an option on the form is checked.

        Args:
            elem: The element to check.

        Returns:
            (bool) True if it is checked.

        """
        return 'raw=134' in elem.get('stream')

    @staticmethod
    def bbox_to_string(bbox):
        """Format a list of bounding box coordinates to a string.

        Args:
            bbox (list): List of coordinates.

        Returns:
            (str) String in format [x1, y1, x2, y2].

        """
        return ', '.join(map(str, bbox))

    @staticmethod
    def bbox_to_list(bbox):
        """Convert a bounding box string to a list of coordinates.

        Args:
            bbox (str): Bounding box in format [x1, y1, x2, y2].

        Returns:
            (str) List of coordinates.

        """
        return bbox.strip('[]').split(', ')

    def find_institution_type(self):
        """Find institution type.

        Returns:
            (list) List of institution types belonging to the institution.

        """
        container = self.pdf.pq('LTRect').filter(self.filter_height)
        if not container:
            return None

        container = container[0]
        entity_forms = self.list_institution_types(container)

        return [entity_forms[i] for i, elem in enumerate(container.findall('LTImage')) if self.option_is_checked(elem)]

    def find_legal_form(self):
        """Find the checked legal form.

        Returns:
            (str) The legal form.

        """
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
        """Run the extraction."""
        self.results = {
            'registered': self.is_registered(),
            'legal form': self.find_legal_form(),
            'institution type': self.find_institution_type()
        }

    def save_results(self):
        """Save the result."""
        entry = self.document.entry
        for key, value in self.results.items():
            entry.add_data_point(key, value)
        self.document.set_processed()
