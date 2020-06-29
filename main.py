from datasets.dataset import Dataset
from endpoints.sparql_connector import SparqlConnector
from graph_analysis.graph_statistics import GraphStatistics


if __name__ == '__main__':
    dataset = Dataset('musicbrainz')
    dataset.parse()
    # TODO: choose endpoint
    conn = SparqlConnector(dataset.endpoints[2][1])
    gs = GraphStatistics(dataset, conn)
    gs.run()
