import pandas as pd


class Frequency:
    def __init__(self, df_tabulated, df_predicate_stats, uri_inforank, min_max_threshold=(0.4, 2)):
        self.dft = df_tabulated
        self.dfs = df_predicate_stats
        self.uri_inforank = uri_inforank
        self.min_max_threshold = min_max_threshold

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
        df_local_pred = df_local_pred.drop(self.uri_inforank)
        return df_local_pred

    def _merge_predicate_frequencies(self, df_local):
        df_result = pd.merge(self.dfs, df_local, on='predicate', how='inner')
        # TODO: rename must be applied in _calculate_local_frequency
        df_result.rename(columns={'object': 'local_frequency'}, inplace=True)
        return df_result.sort_values(by='local_frequency', ascending=False)

    def _calculate_percent_total(self, df):
        df['%_total'] = df.local_frequency / len(self.dft.subject.unique())

    def _filter_by_threshold(self, df):
        min_threshold, max_threshold = self.min_max_threshold
        return df.where((max_threshold >= df['%_total']) & (df['%_total'] >= min_threshold)).dropna()
