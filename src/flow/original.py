from string import Template
from src.endpoints.sparql_query import SparqlQuery


def _build_selection(variables, distinct=False):
    clause = 'select ' + ('distinct ' if distinct else '')
    clause += variables
    return clause


class Original:
    QUERY_TEMPLATE = "$prefixes $selection ?label $dataset where { { $original } . $variable rdfs:label ?label . }"
    SUBQUERY_TEMPLATE = "$selection $dataset where { $graph_pattern }"

    def __init__(self, endpoint, query_parser):
        self.endpoint = endpoint
        self.query_parser = query_parser
        self.final_query = None

    def apply(self):
        q_template = Template(self.QUERY_TEMPLATE)
        s_template = Template(self.SUBQUERY_TEMPLATE)
        single_var = self._build_variables()
        s1 = s_template.substitute(
            selection=_build_selection(single_var),
            dataset=self._build_dataset(),
            graph_pattern=self._build_query_patterns()
        )
        self.final_query = q_template.substitute(
            prefixes=self._build_prefixes(),
            selection=_build_selection(single_var, distinct=True),
            dataset=self._build_dataset(),
            original=s1,
            variable=single_var
        )
        sq = SparqlQuery(self.endpoint, self.final_query)
        df = sq.execute()
        return df

    def _build_prefixes(self):
        return ' '.join(["prefix {}: <{}>".format(alias, uri) for alias, uri in self.query_parser.prefixes])

    def _build_variables(self, three_column=False):
        variables = ' '.join(self.query_parser.variables)
        variables += ' ?predicate ?object' if three_column else ''
        return variables

    def _build_dataset(self):
        if not self.query_parser.dataset:
            return ''
        return "from <{}>".format(self.query_parser.dataset)

    def _build_query_patterns(self):
        return ' . '.join(self.query_parser.query_patterns)
