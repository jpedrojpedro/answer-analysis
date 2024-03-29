import pandas as pd


class Ranking:
    def __init__(self, df_tabulated, uri_inforank):
        self.df = df_tabulated
        self.uri_inforank = uri_inforank

    def apply(self, sort='asc', top=10):
        df_rank = self.df.where(self.df['predicate'] == self.uri_inforank)
        df_rank = df_rank.dropna()
        # TODO: improve performance .lower()
        df_rank['object'] = df_rank['object'].str.lower()
        df_rank['object'] = df_rank['object'].str.replace(',', '.')
        df_rank['object'] = pd.to_numeric(df_rank['object'])
        df_rank = df_rank.sort_values('object', ascending=True if sort == 'asc' else False)
        df_rank = df_rank.iloc[:top]
        return df_rank
