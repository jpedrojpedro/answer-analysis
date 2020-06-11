from pathlib import Path
from configparser import ConfigParser


class Dataset:
    def __init__(self, name):
        self.name = name
        self.endpoints = None
        self.statistics = None
        self.questions = None
        self.boilerplate = None

    def parse(self):
        folder = Path('./datasets/external')
        file = folder / (self.name + '.ini')
        if not file.exists():
            raise FileNotFoundError('Unknown File: ' + str(file))
        config = ConfigParser()
        config.read(file)
        attrs = list(self.__dict__.keys())
        attrs.remove('name')
        for attr in attrs:
            setattr(self, attr, config.items(attr))

    def run(self):
        raise NotImplementedError
