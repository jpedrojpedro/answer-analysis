from src.endpoints.dataset import Dataset
from src.graph_analysis.graph_statistics import GraphStatistics
from src.flow.tabulate import Tabulate
from src.flow.ranking import Ranking
from src.flow.frequency import Frequency
from src.flow.filtering import Filtering
from src.flow.query_parser import QueryParser


# TODO: implement like Rake-Rails
class Main:
    def __init__(self, dataset='brainz.json'):
        self.dataset = Dataset(dataset)
        self.filtered_predicates = []

    def run(self):
        self.dataset.parse()
        endpoint = self.dataset.endpoint
        dest_folder = './src/graph_analysis/' + self.dataset.name
        gs = GraphStatistics(endpoint, self.dataset, dest_folder, 'resources', 'predicates')
        gs.run(load=True)
        question = self.selection_prompt()
        print("Question: {}".format(question.question))
        qp = QueryParser(question.full_sparql_query())
        qp.parse()
        tabulate = Tabulate(endpoint, qp)
        dft = tabulate.apply()
        while True:
            old_dft = dft.copy()
            frequency = Frequency(dft, getattr(gs, 'predicates'), self.dataset.uri_inforank)
            dff = frequency.apply()
            filtering = Filtering(dft, dff, threshold=15, *self.filtered_predicates)
            dft = filtering.apply()
            if old_dft.equals(dft):
                break
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
