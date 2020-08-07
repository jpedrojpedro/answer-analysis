class NewQuestion:
    def __init__(self, df_tabulated, df_frequencies, threshold=5):
        self.dft = df_tabulated
        self.dff = df_frequencies
        self.threshold = threshold

    def generate(self):
        self._filter_candidates()

    def _filter_candidates(self):
        for _idx, row in self.dff.iterrows():
            df_filtered = self.dft.where(self.dft['predicate'] == row['predicate']).dropna()
            df_result = df_filtered.groupby('object')['predicate'].count()
            num_rows = len(df_result.index)
            print("Predicate: {}".format(row['predicate']))
            print("# of rows: {}".format(num_rows))
            if num_rows <= self.threshold:
                print(df_result)
