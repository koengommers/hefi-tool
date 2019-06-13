from finance_document import FinanceDocument
from jellyfish import jaro_winkler
import re

def normalize(index):
    """Returns a normalized index"""
    index = index.lower()
    index = index.replace('som der', 'totaal')
    return re.sub('\(.*\)?','',index)

def create_index_file(file_list, return_file):
    """Input is a list of finance file paths which indexes are used."""
    total_keys = []
    for file in file_list:
        pdf = FinanceDocument(file)
        keys = list(pdf.query()[0].keys())
        if len(total_keys) >= 1:
            for key in keys:
                scores = [jaro_winkler(normalize(key), normalize(x)) for x in total_keys]
                jaro_best = max(scores)
                match = total_keys[scores.index(jaro_best)]
                if jaro_best <= 0.86:
                    total_keys.append(normalize(key))
        else:
            total_keys.extend([normalize(key) for key in keys])

    with open(return_file, 'w', encoding='utf-8') as rfile:
        for key in total_keys:
            rfile.write(str(key))
            rfile.write("\n")
    return keys
