import pdfquery

def handelsregister_filter():
    return float(this.get('y1')) > 700

def legalform_filter():
    return float(this.get('y1')) < 700

def entity_list_filter():
    return float(this.get('height')) > 200

class EntityDocument(object):

    def __init__(self, path):
        self.path = path
        self.pdf = pdfquery.PDFQuery(path)
        self.pdf.load()

    def get_handelsregister(self):
        """ The function returns True or False wheter it is in the """

        results = self.pdf.pq('LTCurve').filter(handelsregister_filter)
        return float(results[1].get('height')) < 6

    def list_entityforms(self, result):
        """The function returns a list of all the entity forms"""

        entityforms = []
        for elem in result:
            if elem.tag != 'LTImage':
                string = ''
                for subelem in elem:
                    string += subelem.text.replace('C ', 'C')
                entityforms.append(string[:-1])
        return entityforms

    def find_entity(self):
        """The function returns a string containing the right entity"""

        result = self.pdf.pq('LTRect').filter(entity_list_filter)
        if result == []:
            return None

        result = result[0]
        entityforms = self.list_entityforms(result)

        return [entityforms[counter] for counter, elem in enumerate(result.findall("LTImage")) if 'raw=134,' in elem.get("stream").split(' ')]

    def find_legalform(self):
        """The function returns a string containing the right legalform"""

        legalforms = ['Publiekrechtelijke rechtspersoon', 'Eenmanszaak',
        'Vennootschap onder firma (VoF)', 'Maatschap', 'Commanditaire vennootschap (CV)',
        'Besloten vennootschap (BV) met Raad van Toezicht / Raad van Commissarissen',
        'Besloten vennootschap (BV) zonder Raad van Toezicht / Raad van Commissarissen',
        'Naamloze vennootschap (NV)', 'Coöperatie en onderlinge waarborgmaatschappij',
        'Stichting', 'Vereniging met volledige rechtsbevoegdheid',
        'Vereniging zonder volledige rechtsbevoegdheid', 'Coöperatieve vereniging',
        'Kerkgenootschap', 'andere rechtsvorm, namelijk:']

        results = self.pdf.pq('LTCurve').filter(legalform_filter)
        for counter, elem in enumerate(results):
            if float(elem.get('height')) < 6:
                return legalforms[counter - 1]
