import pandas as pd
from src.enrichment.ranking import Ranking


class Frequency:
    def __init__(self, df_tabulated, df_predicate_stats):
        self.dft = df_tabulated
        self.dfs = df_predicate_stats

    def apply(self):
        unq_pred = list(self.dft.predicate.unique())
        unq_pred.remove(Ranking.URI_INFORANK)
        df_pred = pd.DataFrame(unq_pred, columns=['predicate'])
        df_result = pd.merge(self.dfs, df_pred, on='predicate', how='inner')
        return df_result
