import re


class QueryParser:
    REGEXP_PREFIX = r"prefix\s+([a-zA-Z0-9]+)\s*:\s*<([a-zA-Z0-9:\/.#_-]+)>"
    REGEXP_VARIABLES = r"(?:select\s+distinct\s+|select\s+)((?:\?[a-zA-Z_]+\s+)+)"
    REGEXP_DATASET = r"from\s*<([a-zA-Z0-9:\/.#_-]+)>"
    REGEXP_QUERY_PATTERN = r"{((.|\n)[^{}]*)}"

    def __init__(self, sparql_query):
        self.sparql_query = sparql_query
        self.prefixes = None
        self.variables = None
        self.dataset = None
        self.query_patterns = None

    def parse(self):
        self._parse_prefixes()
        self._parse_variables()
        self._parse_dataset()
        self._parse_query_patterns()

    def _parse_prefixes(self):
        r_prefixes = re.findall(self.REGEXP_PREFIX, self.sparql_query, re.IGNORECASE)  # list of tuples
        self.prefixes = r_prefixes

    def _parse_variables(self):
        r_variables = re.search(self.REGEXP_VARIABLES, self.sparql_query, re.IGNORECASE)
        variables = r_variables.group(1).strip()
        self.variables = variables.split(' ')

    def _parse_dataset(self):
        r_dataset = re.search(self.REGEXP_DATASET, self.sparql_query, re.IGNORECASE)
        self.dataset = r_dataset.group(1) if r_dataset else None

    def _parse_query_patterns(self):
        r_query_patterns = re.search(self.REGEXP_QUERY_PATTERN, self.sparql_query, re.IGNORECASE)
        query_patterns = r_query_patterns.group(1).strip().split('.')
        self.query_patterns = [qp.strip() for qp in query_patterns if qp.strip()]
