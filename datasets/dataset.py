from pathlib import Path
from configparser import ConfigParser


class Dataset:
    def __init__(self, name):
        self.name = name
        self.endpoints = {}
        self.statistics = {}
        self.questions = []

    def parse(self):
        folder = Path('./datasets/config')
        file = folder / (self.name + '.ini')
        if not file.exists():
            raise FileNotFoundError('Unknown File: ' + str(file))
        config = ConfigParser()
        config.read(file)
        attrs = list(self.__dict__.keys())
        attrs.remove('name')
        for section in config.sections():
            if section in attrs:
                item = {item[0]: item[1] for item in config.items(section)}
                curr = getattr(self, section)
                curr.update(item)
                setattr(self, section, curr)
                continue
            item = {item[0]: item[1] for item in config.items(section)}
            self.questions.append(item)
