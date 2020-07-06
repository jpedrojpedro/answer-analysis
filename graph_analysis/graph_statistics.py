from helper import read_jsonl
from pathlib import Path


class GraphStatistics:
    STEPS = ['resources', 'predicates']

    def __init__(self, dataset, conn):
        self.dataset = dataset
        self.conn = conn
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
        self.conn.execute_query(query)
        self.conn.persist_results(filename)
        setattr(self, step_name, read_jsonl(filename))

    def _clear_analysis(self):
        folder = Path('graph_analysis', 'results')
        for step in self.STEPS:
            filename = folder / (step + '.jsonl')
            if not filename.exists():
                continue
            filename.unlink()
