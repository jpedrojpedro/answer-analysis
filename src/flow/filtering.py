from src import helper


def less_restrictive_faceted(elem):
    pred = elem['predicate']
    opt, opt_amount = sorted(elem['options'], key=lambda e: e[1], reverse=True)[0]
    return opt_amount, pred, opt


class Filtering:
    def __init__(self, df_tabulated, df_frequencies, variable, threshold, sort, *ignore_predicates):
        self.dft = df_tabulated
        self.dff = df_frequencies
        self.variable = variable
        self.threshold = threshold
        self.reverse = True if sort == 'desc' else False
        self.ignore_predicates = ignore_predicates
        self.candidates = []

    def apply(self):
        self._filter_candidates()
        if len(self.candidates) == 0:
            return self.dft, None
        predicate, option = self._select_candidate_and_option()
        df_result = self._filter_results(predicate, option)
        return df_result, predicate

    def all_candidates(self):
        candidates = sorted(self.candidates, key=lambda e: e['amount_uniq_opts'], reverse=self.reverse)
        return candidates

    def _filter_candidates(self):
        for _idx, row in self.dff.iterrows():
            if row['predicate'] in self.ignore_predicates:
                continue
            df_filtered = self.dft.where(self.dft['predicate'] == row['predicate']).dropna()
            df_result = df_filtered.groupby('object')['predicate'].count()
            amount_uniq_opts = len(df_result.index)
            print("Predicate: {}".format(row['predicate']))
            print("# of grouping values: {}".format(amount_uniq_opts))
            if amount_uniq_opts <= self.threshold:
                self.candidates.append({
                    'predicate': row['predicate'],
                    'amount_uniq_opts': amount_uniq_opts,
                    'options': [result for result in df_result.iteritems()]
                })
                print("selected as candidate: {}".format(row['predicate']))
                print(df_result)

    def _select_candidate_and_option(self):
        candidates = self.all_candidates()
        # selected_candidate =
        # approach less restrictive faceted-only | alternative 2
        # sorted(map(less_restrictive_faceted, candidates), key=lambda e: e[0], reverse=True)[0]
        # approach less restrictive predicate and less restrictive faceted | alternative 1
        selected_candidate = sorted(map(less_restrictive_faceted, [candidates[0]]), key=lambda e: e[0], reverse=True)[0]
        # approach most restrictive predicate and less restrictive faceted | short paper
        # sorted(map(less_restrictive_faceted, [candidates[0]]), key=lambda e: e[0], reverse=True)[0]
        option_amount, predicate, option = selected_candidate
        print("selected => predicate: {} | option: {} | matches: {}".format(predicate, option, option_amount))
        return predicate, option

    def _filter_results(self, predicate, option):
        df_filtered = self.dft.where((self.dft['predicate'] == predicate) & (self.dft['object'] == option)).dropna()
        df_result = self.dft[self.dft[self.variable].isin(df_filtered[self.variable].unique())]
        print("tabulated: {}".format(self.dft.shape))
        helper.pretty_print_df(self.dft)
        print("filtered: {}".format(df_filtered.shape))
        helper.pretty_print_df(df_filtered)
        print("result: {}".format(df_result.shape))
        helper.pretty_print_df(df_result)
        print("---------------------------------------------------------------")
        return df_result
