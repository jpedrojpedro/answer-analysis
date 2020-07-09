import unittest
import configparser
from datasets.dataset import Dataset, Question


class DatasetTest(unittest.TestCase):
    def test_parse_raises_exception_file_not_found(self):
        dataset = Dataset('foo', './tests/endpoints/config')
        with self.assertRaises(FileNotFoundError):
            dataset.parse()

    def test_parse_raises_exception_no_section(self):
        dataset = Dataset('bar', './tests/endpoints/config')
        with self.assertRaises(configparser.NoSectionError):
            dataset.parse()

    def test_parse_valid_instance(self):
        dataset = Dataset('got', './tests/endpoints/config')
        dataset.parse()
        self.assertIn('got', dataset.endpoints)
        self.assertEqual(1, len(dataset.questions))
        self.assertIn('amount', dataset.statistics)


class TestQuestion(unittest.TestCase):
    def test_display_prefixes(self):
        init = {
            'question': 'Do you know anything Jon Snow?',
            'keywords': 'Jon Snow',
            'query': 'select distinct ?s where { ?s ?p ?o }'
        }
        prefixes = {
            'dc': 'http://purl.org/dc/elements/1.1/',
            'foaf': 'http://xmlns.com/foaf/0.1/',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'
        }
        expected = [
            "PREFIX dc: <http://purl.org/dc/elements/1.1/>",
            "PREFIX foaf: <http://xmlns.com/foaf/0.1/>",
            "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
        ]
        question = Question(init, prefixes)
        self.assertEqual(question.display_prefixes(), '\n'.join(expected))
