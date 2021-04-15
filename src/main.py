import pandas as pd
from src.endpoints.dataset import Dataset
from src.graph_analysis.graph_statistics import GraphStatistics
from src.flow.tabulate import Tabulate
from src.flow.ranking import Ranking
from src.flow.frequency import Frequency
from src.flow.filtering import Filtering
from src.flow.original import Original
from src.flow.query_parser import QueryParser
from src.flow import heuristic as heuristic_module
from src import helper


class Main:
    def __init__(self, dataset, heuristic):
        self.heuristic = getattr(heuristic_module, 'Heuristic' + heuristic.capitalize())()
        print("Heuristica Escolhida: {}".format(self.heuristic.description))
        self.dataset = Dataset(dataset)
        self.filtered_predicates = []

    def run(self):
        self.dataset.parse()
        endpoint = self.dataset.endpoint
        dest_folder = './src/graph_analysis/' + self.dataset.name
        gs = GraphStatistics(endpoint, self.dataset, dest_folder, 'resources', 'predicates')
        gs.run(load=True)
        question = self.selection_prompt()
        qp = QueryParser(question.full_sparql_query())
        qp.parse()
        original = Original(endpoint, qp)
        dfo = original.apply()
        print("Amostragem da query original")
        print("result: {}".format(dfo.shape))
        helper.pretty_print_df(dfo)
        print("---------------------------------------------------------------")
        tabulate = Tabulate(endpoint, qp)
        dft = tabulate.apply()
        variable = qp.variables[0][1:]  # removing char '?'
        print("Variable: {}".format(variable))
        while True:
            previous_dft = dft.copy()
            frequency = Frequency(dft, getattr(gs, 'predicates'), self.dataset.uri_inforank, self.heuristic.delta)
            dff = frequency.apply()
            filtering = Filtering(
                dft, dff, variable, self.heuristic, *self.filtered_predicates
            )
            dft, curr_predicate = filtering.apply()
            if curr_predicate:
                self.filtered_predicates.append(curr_predicate)
            if self.should_stop(dft, previous_dft, variable, curr_predicate):
                break
        ranking = Ranking(dft, self.dataset.uri_inforank)
        dfr = ranking.apply(sort='desc', top=self.heuristic.beta)
        df = pd.merge(dfr, dfo, on=variable, how='left')
        helper.pretty_print_df(df)

    def selection_prompt(self):
        print("---------------------------------------------------------------")
        options = {idx: question for idx, question in enumerate(self.dataset.questions, start=1)}
        for idx, question in options.items():
            print("{} - {}".format(idx, question.question))
        print("---------------------------------------------------------------")
        id_selected = input("Selecione uma das peguntas acima (7):\t") or '7'
        question = options[int(id_selected)]
        print("Question: {}".format(question.question))
        return question

    def should_stop(self, df, df_prev, variable, predicate):
        keys = [col for col in df.columns if col not in ['predicate', 'object']]
        if len(df[variable].unique()) <= self.heuristic.beta:
            return True
        if helper.check_equality(df_prev, df, keys=keys) and not predicate:
            return True
        return False


if __name__ == '__main__':
    d = input("Informe o dataset desejado (brainz.json):\t") or 'brainz.json'
    h = input("Informe a heuristica desejada (sigma, pi ou omega):\t")
    Main(d, h).run()
