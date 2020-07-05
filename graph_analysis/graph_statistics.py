import jsonlines
from pathlib import Path


def read_jsonl(filename):
    with jsonlines.open(filename) as fp:
        jlist = [jline for jline in fp.iter(type=dict)]
    return jlist


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

    def _run_step(self, step_name):
        queries = [query for name, query in self.dataset.statistics if name == step_name]
        if len(queries) == 0:
            return
        filename = Path('graph_analysis', 'results', step_name + '.jsonl')
        query = queries[0]
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
