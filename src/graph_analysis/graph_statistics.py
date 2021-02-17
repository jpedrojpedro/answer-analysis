import pandas as pd
from pathlib import Path
from src.endpoints.sparql_query import SparqlQuery
from src.helper import persist_results


class GraphStatistics:
    def __init__(self, endpoint, dataset, dest_folder='./src/graph_analysis/results', *steps):
        self.endpoint = endpoint
        self.dataset = dataset
        self.dest_folder = dest_folder
        self.steps = steps
        for step in self.steps:
            setattr(self, step, None)

    def run(self, load=False):
        if load:
            self._load()
            return
        self._clear_analysis()
        for step in self.steps:
            self._run_step(step)

    def _load(self):
        for step in self.steps:
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
        for step in self.steps:
            filename = folder / (step + '.jsonl')
            if not filename.exists():
                continue
            filename.unlink()
