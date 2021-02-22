from string import Template
from src.endpoints.sparql_query import SparqlQuery


def _build_selection(variables, distinct=False):
    clause = 'select ' + ('distinct ' if distinct else '')
    clause += variables
    return clause


class Tabulate:
    QUERY_TEMPLATE = "$prefixes $selection $dataset where { { $original } . { $tabulated } }"
    SUBQUERY_TEMPLATE = "$selection $dataset where { $graph_pattern }"
    FILTER_TEMPLATE = "$variable ?predicate ?object . filter(isLiteral(?object))"

    def __init__(self, endpoint, query_parser):
        self.endpoint = endpoint
        self.query_parser = query_parser

    def apply(self):
        q_template = Template(self.QUERY_TEMPLATE)
        s_template = Template(self.SUBQUERY_TEMPLATE)
        single_var = self._build_variables()
        three_vars = self._build_variables(three_column=True)
        s1 = s_template.substitute(
            selection=_build_selection(single_var),
            dataset=self._build_dataset(),
            graph_pattern=self._build_query_patterns()
        )
        s2 = s_template.substitute(
            selection=_build_selection(three_vars),
            dataset=self._build_dataset(),
            graph_pattern=self._build_tabulated_query_pattern(single_var)
        )
        final_query = q_template.substitute(
            prefixes=self._build_prefixes(),
            selection=_build_selection(three_vars, distinct=True),
            dataset=self._build_dataset(),
            original=s1,
            tabulated=s2
        )
        sq = SparqlQuery(self.endpoint, final_query)
        df = sq.execute()
        return df

    def _build_prefixes(self):
        return ' '.join(["prefix {}: <{}>".format(alias, uri) for alias, uri in self.query_parser.prefixes])

    def _build_variables(self, three_column=False):
        variables = ' '.join(self.query_parser.variables)
        variables += ' ?predicate ?object' if three_column else ''
        return variables

    def _build_dataset(self):
        if self.query_parser.dataset:
            return "from <{}>".format(self.query_parser.dataset)

    def _build_query_patterns(self):
        return ' . '.join(self.query_parser.query_patterns)

    def _build_tabulated_query_pattern(self, variable):
        f_template = Template(self.FILTER_TEMPLATE)
        return f_template.substitute(variable=variable)
