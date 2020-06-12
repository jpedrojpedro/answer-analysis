import jsonlines
from pathlib import Path
from string import Template


def _read_jsonl(filename):
    with jsonlines.open(filename) as fp:
        jlist = [jline for jline in fp.iter(type=dict)]
    return jlist


class GraphStatistics:
    STEPS = ['classes', 'instances', 'relationships']

    def __init__(self, dataset, conn):
        self.dataset = dataset
        self.conn = conn
        self.classes = None

    def run(self):
        self._clear_analysis()
        self._run_classes()
        self._run_instances()

    def _run_classes(self):
        queries = [query for name, query in self.dataset.statistics if name == 'classes']
        if len(queries) == 0:
            return
        filename = Path('graph_analysis', 'classes.jsonl')
        query = queries[0]
        self.conn.execute_query(query)
        self.conn.persist_results(filename)
        self.classes = _read_jsonl(filename)

    def _run_instances(self):
        queries = [query for name, query in self.dataset.statistics if name == 'instances']
        if len(queries) == 0:
            return
        filename = Path('graph_analysis', 'instances.jsonl')
        query = queries[0]
        for klass in self.classes:
            tquery = Template(query)
            self.conn.execute_query(tquery.substitute(klass=klass['class']))
            self.conn.persist_results(filename, append=True)

    def _clear_analysis(self):
        folder = Path('graph_analysis')
        for step in self.STEPS:
            filename = folder / (step + '.jsonl')
            if not filename.exists():
                continue
            filename.unlink()
