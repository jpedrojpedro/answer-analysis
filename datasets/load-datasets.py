from pathlib import Path
from franz.openrdf.connect import ag_connect
from franz.openrdf.rio.rdfformat import RDFFormat


AGRAPH_HOST = 'localhost'
AGRAPH_PORT = 10035
AGRAPH_USER = 'q&a'
AGRAPH_PASSWORD = '102030'


if __name__ == '__main__':
    conn = ag_connect('answer-analysis', host=AGRAPH_HOST, port=AGRAPH_PORT, user=AGRAPH_USER, password=AGRAPH_PASSWORD)
    folder = Path('.') / 'datasets'
    for file in list(folder.glob('*.rdf')):
        path = str(file.absolute())
        conn.add(path, base=None, format=RDFFormat.RDFXML, contexts=None)
