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
    def __init__(self, name, folder='./endpoints/config'):
        self.name = name
        self.folder = folder
        self.endpoints = {}
        self.statistics = {}
        self.questions = []

    def parse(self):
        folder = Path(self.folder)
        file = folder / (self.name + '.ini')
        if not file.exists():
            raise FileNotFoundError('Unknown File: ' + str(file))
        config = ConfigParser()
        config.read(file)
        attrs = list(self.__dict__.keys())
        attrs.remove('name')
        # may raise error
        prefixes = {item[0]: item[1] for item in config.items('prefixes')}
        for section in config.sections():
            if section == 'prefixes':
                continue
            item = {item[0]: item[1] for item in config.items(section)}
            if section in attrs:
                curr = getattr(self, section)
                curr.update(item)
                setattr(self, section, curr)
                continue
            question = Question(item, prefixes)
            self.questions.append(question)
