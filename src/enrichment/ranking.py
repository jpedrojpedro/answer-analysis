import pandas as pd


class Ranking:
    # TODO: change this URI
    URI_INFORANK = 'http://www.imdb.quira/inforank'

    def __init__(self, df_tabulated):
        self.df = df_tabulated

    def apply(self):
        df_rank = self.df.where(self.df['predicate'] == self.URI_INFORANK)
        df_rank = df_rank.dropna()
        # TODO: improve performance .lower()
        df_rank['object'] = df_rank['object'].str.lower()
        df_rank['object'] = df_rank['object'].str.replace(',', '.')
        df_rank['object'] = pd.to_numeric(df_rank['object'])
        df_rank = df_rank.sort_values('object', ascending=False)
        return df_rank
