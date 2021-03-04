import pandas as pd


def persist_results(df, filename, append=False):
    with open(filename, 'w' if not append else 'a') as fp:
        jsonl = df.to_json(orient='records', lines=True)
        fp.write(jsonl)


def check_equality(df1, df2, keys):
    if df1.empty and df2.empty:  # there is a bug comparing empty dataframes on Pandas
        if df1.shape == df2.shape and sorted(list(df1.columns)) == sorted(list(df2.columns)):
            return True
        return False
    df1 = df1.sort_values(by=keys).reset_index(drop=True)
    df2 = df2.sort_values(by=keys).reset_index(drop=True)
    return pd.DataFrame.equals(df1, df2)


def pretty_print_df(df, limit=40):
    cols = df.columns
    template = ' | '.join([f"{{{col}:50}}" for col in cols])
    print(template.format(**{col: col for col in cols}))
    for _idx, row in df.head(limit).iterrows():
        print(template.format(**{col: row[col] for col in cols}))
