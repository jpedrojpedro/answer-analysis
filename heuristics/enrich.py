import re
import tempfile
from string import Template
from helper import read_jsonl


class Enrich:
    REGEX_VARIABLE = r"(SELECT\s+|DISTINCT\s+)(\?[a-zA-Z_]+)(\sFROM\s+[a-z<>:\/.]+\s+|\s+WHERE)"
    SPARQL_TEMPLATE = """
        $prefixes
        select distinct $variable ?p ?o
        where {
          { $subquery }
          $variable ?p ?o .
          filter(isLiteral(?o)) .
        }
    """

    def __init__(self, question, conn):
        self.question = question
        self.conn = conn
        self.variable = None
        self.enriched_query = None
        self.results = None

    def apply(self):
        self._set_variable()
        self._set_enriched_query()
        self.conn.execute_query(self.enriched_query)
        tmp_file = tempfile.TemporaryFile()
        self.conn.persist_results(tmp_file)
        self.results = read_jsonl(tmp_file)

    def _set_variable(self):
        result = re.search(self.REGEX_VARIABLE, self.question.query, re.IGNORECASE)
        if result is None:
            return
        self.variable = result.group(2)

    def _set_enriched_query(self):
        template = Template(self.SPARQL_TEMPLATE)
        self.enriched_query = template.substitute(
            prefixes=self.question.display_prefixes(), variable=self.variable, subquery=self.question.query
        )
