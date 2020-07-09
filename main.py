import pandas as pd
from datasets.dataset import Dataset
from graph_analysis.graph_statistics import GraphStatistics
from heuristics.enrich import Enrich


def match_predicates(df_enriched, df_pred_stats):
    unq_pred = df_enriched.predicate.unique()
    df_pred = pd.DataFrame(unq_pred, columns=['predicate'])
    df_result = pd.merge(df_pred_stats, df_pred, on='predicate', how='inner')
    return df_result


# TODO: implement like Rake-Rails
if __name__ == '__main__':
    dataset = Dataset('musicbrainz')
    dataset.parse()
    endpoint = dataset.endpoints['linkedbrainz']
    gs = GraphStatistics(endpoint, dataset)
    gs.load()  # gs.run()
    for idx, question in enumerate(dataset.questions, start=1):
        print("----------{}----------".format(idx))
        print("Question: {}".format(question.question))
        enrich = Enrich(endpoint, question)
        dfe = enrich.apply()
        df_match = match_predicates(dfe, gs.predicates)
        print(df_match.head(20))
