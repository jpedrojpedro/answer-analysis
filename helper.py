import jsonlines


def read_jsonl(filename):
    with jsonlines.open(filename) as fp:
        jlist = [jline for jline in fp.iter(type=dict)]
    return jlist
