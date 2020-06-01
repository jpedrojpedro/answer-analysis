import re
import json
from SPARQLWrapper import SPARQLWrapper, JSON
from pathlib import Path


def parse_endpoint_and_questions(dataset='musicbrainz', meta=False):
    folder = Path('./questions')
    file = folder / (dataset + '.json')
    if not file.exists():
        raise FileNotFoundError('Unknown File: ' + str(file))
    with open(file, 'r') as fp:
        info = json.load(fp)
    endpoint = info['meta']['endpoint']
    if meta:
        return endpoint, info['meta']['questions']
    return endpoint, info['questions']


def separate_prefix_and_class(uri):
    regex = r'^([a-z0-9\/.:-]+)((\/|#)[a-zA-Z0-9]+)$'
    res = re.search(regex, uri)
    prefix = res.group(1)
    klass = res.group(2)
    return prefix, klass


if __name__ == '__main__':
    try:
        folder = Path('./output')
        url, questions = parse_endpoint_and_questions(meta=True)
        sparql = SPARQLWrapper(url)
        for question in questions:
            sparql.setQuery(question['question'])
            sparql.setReturnFormat(JSON)
            output = sparql.query().convert()
            results = output['results']['bindings']
            print("{}: {} results found".format(question['id'], len(results)))
            if len(results) > 0:
                file = folder / (question['id'] + '.out')
                with open(file, 'w') as fp:
                    keys = results[0].keys()
                    template = ' | '.join(['{:40}'] * len(keys))
                    line = template.format(*keys)
                    print(line)
                    fp.write(line + '\n')
                    for result in results:
                        line = template.format(*[result[key]['value'] for key in keys])
                        print(line)
                        fp.write(line + '\n')
    # TODO: handle exceptions raised by sparql.query()
    except FileNotFoundError as e1:
        print(e1)
    except json.JSONDecodeError as e2:
        print('parse_endpoint_and_questions: {} reading json questions file'.format(type(e2)))
        print(e2)
    except TypeError as e3:
        print('parse_endpoint_and_questions: {} reading json questions file'.format(type(e3)))
        print(e3)
