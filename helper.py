import jsonlines


def read_jsonl(filename):
    with jsonlines.open(filename) as fp:
        jlist = [jline for jline in fp.iter(type=dict)]
    return jlist


def persist_results(df, filename, append=False):
    with open(filename, 'w' if not append else 'a') as fp:
        jsonl = df.to_json(orient='records', lines=True)
        fp.write(jsonl)
