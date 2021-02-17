class NewQuery:
    def __init__(self, df_tabulated, df_frequencies, prior_query, threshold=5):
        self.dft = df_tabulated
        self.dff = df_frequencies
        self.prior_query = prior_query
        self.threshold = threshold
        self.candidates = []

    def generate(self):
        self._filter_candidates()

    def _filter_candidates(self):
        for _idx, row in self.dff.iterrows():
            df_filtered = self.dft.where(self.dft['predicate'] == row['predicate']).dropna()
            df_result = df_filtered.groupby('object')['predicate'].count()
            num_grouping_values = len(df_result.index)
            print("Predicate: {}".format(row['predicate']))
            print("# of grouping values: {}".format(num_grouping_values))
            if num_grouping_values <= self.threshold:
                self.candidates.append({'predicate': row['predicate'], 'num_grouping_values': num_grouping_values})
                print(df_result)
        self.candidates.sort(key=lambda e: e['num_grouping_values'], reverse=True)
        print(self.candidates)

    # def _build_new_query(self):
    #     candidate = self.candidates[0]
    #     pass
