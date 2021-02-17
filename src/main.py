from src.endpoints.dataset import Dataset
from src.graph_analysis.graph_statistics import GraphStatistics
from src.enrichment.tabulate import Tabulate
from src.enrichment.ranking import Ranking
from src.enrichment.frequency import Frequency
from src.enrichment.new_query import NewQuery


# TODO: implement like Rake-Rails
class Main:
    def __init__(self, dataset='brainz.json'):
        self.dataset = Dataset(dataset)

    def run(self):
        self.dataset.parse()
        endpoint = self.dataset.endpoint
        dest_folder = './src/graph_analysis/' + self.dataset.name
        gs = GraphStatistics(endpoint, self.dataset, dest_folder, 'resources', 'predicates')
        gs.run(load=True)
        question = self.selection_prompt()
        print("Question: {}".format(question.question))
        tabulate = Tabulate(endpoint, question)
        dft = tabulate.apply()
        print(tabulate.enriched_query)
        frequency = Frequency(dft, getattr(gs, 'predicates'), self.dataset.uri_inforank)
        dff = frequency.apply()
        new_query = NewQuery(dft, dff, tabulate.enriched_query, threshold=10)
        new_query.generate()
        # TODO: step ranking only called when no new question can be formulated
        ranking = Ranking(dft, self.dataset.uri_inforank)
        dfr = ranking.apply()
        print(dfr)

    def selection_prompt(self):
        print("---------------------")
        options = {idx: question for idx, question in enumerate(self.dataset.questions, start=1)}
        for idx, question in options.items():
            print("{} - {}".format(idx, question.question))
        print("---------------------")
        id_selected = input("Selecione uma das peguntas acima (7):\t") or '7'
        return options[int(id_selected)]


if __name__ == '__main__':
    config = input("Informe o dataset desejado (brainz.json):\t") or 'brainz.json'
    Main(config).run()
