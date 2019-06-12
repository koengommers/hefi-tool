import xml.etree.ElementTree as etree 
    
class EntityDocument(object):

    def __init__(self, path):
        self.path = path

        tree = etree.parse(path)  
        self.root = tree.getroot()[0]
    
    def get_LTCurve(self):
        """ The function returns two objects consisting of xml code: one 
            containing the answer on the question: "Is deze entiteit opgenomen 
            in het Handelsregister" and the other containing which legal form it 
            is """

        return [elem for elem in self.root if elem.find('LTCurve') != None]
    
    def get_LTImage(self):
        """ The function returns one object containing the xml code to which 
            entity this company is the handelsregister """
        list_objects = [elem for elem in self.root if elem.find('LTImage') != None]

        if len(list_objects) == 1:
            return None
        else:
            return list_objects[1]
    
    def get_handelsregister(self):
        """ The function returns ja or nee wheter it is in the """

        legalform_xml = self.get_LTCurve()[0]

        LTCurves = legalform_xml.findall("LTCurve")
        if LTCurves[0].find('LTCurve') != None:
            return 'ja'
        else: 
            return 'nee'

    def list_entityforms(self, xml_code):
        """ The function returns a list of all the entity forms """

        entityforms = []
        for elem in xml_code:
            if elem.tag != 'LTImage':
                string = ''
                for subelem in elem:
                    string += subelem.text.replace('C ', 'C')
                entityforms.append(string)
        return entityforms

    def find_entity(self):
        """ The function returns a string containing the right entity """

        entity_xml = self.get_LTImage()
        if entity_xml == None:
            return 'n.v.t.'

        entityforms = self.list_entityforms(entity_xml)

        for counter, elem in enumerate(entity_xml.findall("LTImage")):
            if 'raw=134,' in elem.get("stream").split(' '):
                index = counter
                break
        return entityforms[index]

    def find_legalform(self):
        """ The function returns a string containing the right legalform """

        legalforms = ['Publiekrechtelijke rechtspersoon', 'Eenmanszaak', 
        'Vennootschap onder firma (VoF)', 'Maatschap', 'Commanditaire vennootschap (CV)',
        'Besloten vennootschap (BV) met Raad van Toezicht / Raad van Commissarissen', 
        'Besloten vennootschap (BV) zonder Raad van Toezicht / Raad van Commissarissen', 
        'Naamloze vennootschap (NV)', 'Coöperatie en onderlinge waarborgmaatschappij', 
        'Stichting', 'Vereniging met volledige rechtsbevoegdheid', 
        'Vereniging zonder volledige rechtsbevoegdheid', 'Coöperatieve vereniging', 
        'Kerkgenootschap', 'andere rechtsvorm, namelijk:']

        legalform_xml = self.get_LTCurve()[1]

        for counter,elem in enumerate(legalform_xml.findall("LTCurve")):
            if elem.find('LTCurve') != None:
                index = counter
                break
        return legalforms[index]

test = EntityDocument('testpdf9.xml')


print(test.find_entity())
print(test.find_legalform())

