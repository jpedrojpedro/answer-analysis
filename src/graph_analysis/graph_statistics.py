import pandas as pd
from pathlib import Path
from src.endpoints.sparql_query import SparqlQuery
from src.helper import persist_results


class GraphStatistics:
    STEPS = ['resources', 'predicates']

    def __init__(self, endpoint, dataset, dest_folder='./src/graph_analysis/results'):
        self.endpoint = endpoint
        self.dataset = dataset
        self.dest_folder = dest_folder
        for step in self.STEPS:
            setattr(self, step, None)

    def run(self):
        self._clear_analysis()
        for step in self.STEPS:
            self._run_step(step)

    def load(self):
        for step in self.STEPS:
            folder = Path(self.dest_folder)
            filename = folder / (step + '.jsonl')
            if not filename.exists():
                continue
            setattr(self, step, pd.read_json(filename, lines=True))

    def _run_step(self, step_name):
        query = self.dataset.statistics.get(step_name)
        if query is None:
            return
        folder = Path(self.dest_folder)
        filename = folder / (step_name + '.jsonl')
        sq = SparqlQuery(self.endpoint, query)
        df = sq.execute()
        persist_results(df, filename)
        setattr(self, step_name, df)

    def _clear_analysis(self):
        folder = Path(self.dest_folder)
        for step in self.STEPS:
            filename = folder / (step + '.jsonl')
            if not filename.exists():
                continue
            filename.unlink()
