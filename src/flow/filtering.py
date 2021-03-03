class Filtering:
    def __init__(self, df_tabulated, df_frequencies, variable, threshold, *ignore_predicates):
        self.dft = df_tabulated
        self.dff = df_frequencies
        self.variable = variable
        self.threshold = threshold
        self.ignore_predicates = ignore_predicates
        self.candidates = []

    def apply(self):
        self._filter_candidates()
        if len(self.candidates) == 0:
            return self.dft
        predicate = self._select_candidate()
        df_result = self._filter_results(predicate)
        return df_result, predicate

    def _filter_candidates(self):
        for _idx, row in self.dff.iterrows():
            if row['predicate'] in self.ignore_predicates:
                continue
            df_filtered = self.dft.where(self.dft['predicate'] == row['predicate']).dropna()
            df_result = df_filtered.groupby('object')['predicate'].count()
            num_grouping_values = len(df_result.index)
            # print("Predicate: {}".format(row['predicate']))
            # print("# of grouping values: {}".format(num_grouping_values))
            if num_grouping_values <= self.threshold:
                self.candidates.append({'predicate': row['predicate'], 'num_grouping_values': num_grouping_values})
                # print(df_result)

    def _select_candidate(self, reverse=True):
        candidates = sorted(self.candidates, key=lambda e: e['num_grouping_values'], reverse=reverse)
        candidates = [c['predicate'] for c in candidates]
        return candidates[0]

    def _filter_results(self, predicate):
        df_filtered = self.dft.where(self.dft['predicate'] == predicate).dropna()
        df_result = self.dft[self.dft[self.variable].isin(df_filtered[self.variable].unique())]
        print("selected predicate: {}".format(predicate))
        print("tabulated: {}".format(self.dft.shape))
        print("filtered: {}".format(df_filtered.shape))
        print("result: {}".format(df_result.shape))
        print("---------------------")
        return df_result
