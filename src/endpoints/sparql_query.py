import io
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, CSV, POST, POSTDIRECTLY


class SparqlQuery:
    def __init__(self, endpoint, query):
        self.endpoint = endpoint
        self.query = query

    def execute(self):
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(self.query)
        sparql.setTimeout(600)  # 10 minutes
        sparql.setOnlyConneg(True)
        sparql.addCustomHttpHeader("Content-type", "application/sparql-query")
        sparql.addCustomHttpHeader("Accept", "text/csv")
        sparql.setMethod(POST)
        sparql.setRequestMethod(POSTDIRECTLY)
        sparql.setReturnFormat(CSV)
        results = sparql.queryAndConvert()
        decoded_csv = io.StringIO(results.decode("utf-8"))
        df = pd.read_csv(decoded_csv, sep=",")
        return df
