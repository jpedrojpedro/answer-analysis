from pathlib import Path
from endpoints.sparql_query import SparqlQuery
from helper import read_jsonl, persist_results


class GraphStatistics:
    STEPS = ['resources', 'predicates']

    def __init__(self, endpoint, dataset):
        self.endpoint = endpoint
        self.dataset = dataset
        for step in self.STEPS:
            setattr(self, step, None)

    def run(self):
        self._clear_analysis()
        for step in self.STEPS:
            self._run_step(step)

    def load(self):
        for step in self.STEPS:
            filename = Path('graph_analysis', 'results', step + '.jsonl')
            if not filename.exists():
                continue
            setattr(self, step, read_jsonl(filename))

    def _run_step(self, step_name):
        query = self.dataset.statistics.get(step_name)
        if query is None:
            return
        filename = Path('graph_analysis', 'results', step_name + '.jsonl')
        sq = SparqlQuery(self.endpoint, query)
        df = sq.execute()
        persist_results(df, filename)
        setattr(self, step_name, df)

    def _clear_analysis(self):
        folder = Path('graph_analysis', 'results')
        for step in self.STEPS:
            filename = folder / (step + '.jsonl')
            if not filename.exists():
                continue
            filename.unlink()
