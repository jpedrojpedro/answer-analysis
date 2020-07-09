from datasets.dataset import Dataset
from graph_analysis.graph_statistics import GraphStatistics
from heuristics.enrich import Enrich


# TODO: implement like Rake-Rails
if __name__ == '__main__':
    dataset = Dataset('musicbrainz')
    dataset.parse()
    endpoint = dataset.endpoints['linkedbrainz']
    gs = GraphStatistics(endpoint, dataset)
    gs.load()  # gs.run()
    for question in dataset.questions:
        enrich = Enrich(endpoint, question)
        enrich.apply()
        enrich.results.head(20)
        break
