import pandas as pd
from src.enrichment.ranking import Ranking


class Frequency:
    def __init__(self, df_tabulated, df_predicate_stats, threshold=0.4):
        self.dft = df_tabulated
        self.dfs = df_predicate_stats
        self.threshold = threshold

    def apply(self):
        self._guarantee_column_names('dft', 'subject', 'predicate', 'object')
        self._guarantee_column_names('dfs', 'predicate', 'global_frequency')
        df_local_pred = self._calculate_local_frequency()
        df_result = self._merge_predicate_frequencies(df_local_pred)
        self._calculate_percent_total(df_result)
        df_result = self._filter_by_threshold(df_result)
        return df_result

    def _guarantee_column_names(self, df_name, *cols):
        df = getattr(self, df_name)
        columns = {df.columns[idx]: col for idx, col in enumerate(cols)}
        setattr(self, df_name, df.rename(columns=columns))

    def _calculate_local_frequency(self):
        df_local_pred = self.dft.groupby('predicate')['object'].count()
        df_local_pred = df_local_pred.drop(Ranking.URI_INFORANK)
        return df_local_pred

    def _merge_predicate_frequencies(self, df_local):
        df_result = pd.merge(self.dfs, df_local, on='predicate', how='inner')
        # TODO: rename must be applied in _calculate_local_frequency
        df_result.rename(columns={'object': 'local_frequency'}, inplace=True)
        return df_result.sort_values(by='local_frequency', ascending=False)

    def _calculate_percent_total(self, df):
        df['%_total'] = df.local_frequency / len(self.dft.subject.unique())

    def _filter_by_threshold(self, df):
        return df.where(df['%_total'] >= self.threshold).dropna()
