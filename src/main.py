from src.endpoints.dataset import Dataset
from src.graph_analysis.graph_statistics import GraphStatistics
from src.enrichment.tabulate import Tabulate
from src.enrichment.ranking import Ranking
from src.enrichment.frequency import Frequency


# TODO: implement like Rake-Rails
class Main:
    def __init__(self, dataset='musicbrainz'):
        self.dataset = dataset

    def run(self):
        dataset = Dataset(self.dataset)
        dataset.parse()
        endpoint = dataset.endpoints['linkedbrainz']
        gs = GraphStatistics(endpoint, dataset)
        gs.run(load=True)
        for idx, question in enumerate(dataset.questions, start=1):
            print("----------{}----------".format(idx))
            print("Question: {}".format(question.question))
            tabulate = Tabulate(endpoint, question)
            dft = tabulate.apply()
            ranking = Ranking(dft)
            dfr = ranking.apply()
            frequency = Frequency(dft, gs.predicates)
            dff = frequency.apply()


if __name__ == '__main__':
    Main().run()
