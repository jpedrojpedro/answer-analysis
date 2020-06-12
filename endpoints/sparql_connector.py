import jsonlines
from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlConnector:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.sparql = SPARQLWrapper(self.endpoint)
        self.results = None

    # TODO: try to set timeout
    def execute_query(self, question, output=JSON):
        self.sparql.setQuery(question)
        self.sparql.setReturnFormat(output)
        results = self.sparql.queryAndConvert()
        self.results = results['results']['bindings']

    def display_results(self):
        if not self.results:
            return
        keys = self.results[0].keys()
        template = ' | '.join(['{:30}'] * len(keys))
        line = template.format(*keys)
        print(line)
        for result in self.results:
            line = template.format(*[result.get(key, {'value': ''})['value'] for key in keys])
            print(line)

    def persist_results(self, filename, append=False):
        if not self.results:
            return
        with jsonlines.open(filename, 'w' if not append else 'a') as fp:
            for result in self.results:
                d = {key: result[key]['value'] for key in result.keys()}
                fp.write(d)
