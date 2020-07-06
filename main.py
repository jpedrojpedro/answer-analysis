from datasets.dataset import Dataset
from endpoints.sparql_connector import SparqlConnector
from graph_analysis.graph_statistics import GraphStatistics
from heuristics.enrich import Enrich


if __name__ == '__main__':
    dataset = Dataset('musicbrainz')
    dataset.parse()
    conn = SparqlConnector(dataset.endpoints['linkedbrainz'])
    gs = GraphStatistics(dataset, conn)
    gs.load()  # gs.run()
    for question in dataset.questions:
        enrich = Enrich(question, conn)
        enrich.apply()
        for result in enrich.results[:10]:
            print(result)
        break
