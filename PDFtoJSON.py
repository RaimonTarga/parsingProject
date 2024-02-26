import os
import json
import PyPDF2
from PyPDF2 import PdfReader

FILE_NAME = 'Listados.pdf'
OUTPUT_FILE_NAME = 'Listados.json'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
FILE_PATH = os.path.join(ROOT_DIR, FILE_NAME)
OUTPUT_PATH = os.path.join(ROOT_DIR, OUTPUT_FILE_NAME)

reader = PdfReader(FILE_PATH)

data = []
for page in reader.pages:
    for line in page.extract_text().splitlines():
        if (line[0] != 'I'):
            values = line.split()
            entry = {}
            entry['ID_Cliente'] = values[0]
            entry['ID_Facturacion'] = values[1]
            entry['N_Articulos'] = values[2]
            entry['Cod_Internacional'] = values[3]
            entry['Generar_factura'] = (values[4] == 'S')
            print(json.dumps(entry))
            data.append(entry)

with open(OUTPUT_PATH, 'w') as outfile:
    outfile.write(json.dumps(data))
