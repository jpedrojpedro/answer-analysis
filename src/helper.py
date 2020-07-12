def persist_results(df, filename, append=False):
    with open(filename, 'w' if not append else 'a') as fp:
        jsonl = df.to_json(orient='records', lines=True)
        fp.write(jsonl)
