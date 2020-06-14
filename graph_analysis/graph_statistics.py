import jsonlines
from pathlib import Path
from string import Template


def read_jsonl(filename):
    with jsonlines.open(filename) as fp:
        jlist = [jline for jline in fp.iter(type=dict)]
    return jlist


class GraphStatistics:
    STEPS = ['classes', 'instances', 'relationships']

    def __init__(self, dataset, conn):
        self.dataset = dataset
        self.conn = conn
        self.classes = None
        self.instances = None

    def run(self):
        # TODO: implement some kind of progress bar
        self._clear_analysis()
        self._run_classes()
        self._run_instances()
        self._run_relationships()

    def _run_classes(self):
        queries = [query for name, query in self.dataset.statistics if name == 'classes']
        if len(queries) == 0:
            return
        filename = Path('graph_analysis', 'results', 'classes.jsonl')
        query = queries[0]
        self.conn.execute_query(query)
        self.conn.persist_results(filename)
        self.classes = read_jsonl(filename)

    def _run_instances(self):
        queries = [query for name, query in self.dataset.statistics if name == 'instances']
        if len(queries) == 0:
            return
        filename = Path('graph_analysis', 'results', 'instances.jsonl')
        query = queries[0]
        for klass in self.classes:
            tquery = Template(query)
            self.conn.execute_query(tquery.substitute(klass=klass['class']))
            self.conn.persist_results(filename, append=True)
        self.instances = read_jsonl(filename)

    def _run_relationships(self):
        queries = [query for name, query in self.dataset.statistics if name == 'relationships']
        if len(queries) == 0:
            return
        filename = Path('graph_analysis', 'results', 'relationships.jsonl')
        query = queries[0]
        for klass_1 in self.classes:
            for klass_2 in self.classes:
                if klass_1 == klass_2:
                    continue
                try:
                    k1 = klass_1['class']
                    k2 = klass_2['class']
                    print("{} vs {}".format(k1, k2))
                    i1 = [instance for instance in self.instances if instance['class'] == k1]
                    i2 = [instance for instance in self.instances if instance['class'] == k2]
                    a1 = int(i1[0]['amount'])
                    a2 = int(i2[0]['amount'])
                    l1 = a1 // 10 if a1 >= 10 else a1
                    l2 = a2 // 10 if a2 >= 10 else a2
                    tquery = Template(query)
                    self.conn.execute_query(
                        tquery.substitute(
                            klass_1=k1, klass_2=k2, limit_k1=l1, limit_k2=l2
                        )
                    )
                    self.conn.persist_results(filename, append=True)
                # TODO: improve this exception handling
                except Exception:
                    continue

    def _clear_analysis(self):
        folder = Path('graph_analysis', 'results')
        for step in self.STEPS:
            filename = folder / (step + '.jsonl')
            if not filename.exists():
                continue
            filename.unlink()
