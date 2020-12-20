import json
from pathlib import Path
from configparser import ConfigParser


# TODO: implement dataclasses
class Question:
    def __init__(self, q_ini, prefixes):
        self.question = q_ini['question']
        self.keywords = q_ini['keywords']
        self.query = q_ini['query']
        self.prefixes = ["PREFIX {}: <{}>".format(prefix, uri) for prefix, uri in prefixes.items()]

    def display_prefixes(self):
        return '\n'.join(self.prefixes)


class Dataset:
    def __init__(self, name, folder='./src/endpoints/config'):
        self.name = name
        self.folder = folder
        self.endpoint = None
        self.statistics = None
        self.questions = None

    def parse(self):
        folder = Path(self.folder)
        file = folder / self.name
        if not file.exists():
            raise FileNotFoundError('Unknown File: ' + str(file))
        name, ext = self.name.split('.')
        getattr(self, 'parse_' + ext)(file)

    def parse_ini(self, file):
        config = ConfigParser()
        config.read(file)
        prefixes = {item[0]: item[1] for item in config.items('prefixes')}
        self.endpoint = [item[1] for item in config.items('endpoints')][0]
        self.statistics = {item[0]: item[1] for item in config.items('statistics')}
        questions = []
        for section in config.sections():
            if section in ['prefixes', 'endpoints', 'statistics']:
                continue
            item = {item[0]: item[1] for item in config.items(section)}
            question = Question(item, prefixes)
            questions.append(question)
        self.questions = questions

    def parse_json(self, file):
        config = json.loads(file.read_bytes())
        self.endpoint = config['endpoint']
        self.statistics = config['statistics']
        questions = config['questions']
        prefixes = config['prefixes']
        self.questions = [Question(question, prefixes) for question in questions]
