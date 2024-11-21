import unittest
from unittest.mock import patch, mock_open
import json
from data_loader import DataLoader
from models.Issue import Issue
from models.State import State

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        # Reset the global _ISSUES variable before each test
        import data_loader
        data_loader._ISSUES = None

    @patch('data_loader.config')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_issues(self, mock_file, mock_config):
        # Mock the data path
        mock_config.get_parameter.return_value = 'fake_path.json'

        sample_issues = [
            {
                "url": "https://github.com/scikit-learn/scikit-learn/issues/28994",
                "creator": "jeremycg",
                "labels": ["Documentation"],
                "state": "open",
                "assignees": [],
                "title": "StratifiedShuffleSplit requires three copies of a lower class, rather than 2",
                "text": "Sample issue text...",
                "number": 28994,
                "created_date": "2024-05-10T18:38:17+00:00",
                "updated_date": "2024-05-16T18:27:00+00:00",
                "timeline_url": "https://api.github.com/repos/scikit-learn/scikit-learn/issues/28994/timeline",
                "events": [
                    {
                        "event_type": "labeled",
                        "author": "jeremycg",
                        "event_date": "2024-05-10T18:38:18+00:00",
                        "label": "Bug"
                    }
                ]
            }
        ]

        mock_file.return_value.read.return_value = json.dumps(sample_issues)

        loader = DataLoader()
        issues = loader.get_issues()
        self.assertEqual(len(issues), 1)
        self.assertIsInstance(issues[0], Issue)
        self.assertEqual(issues[0].url, 'https://github.com/scikit-learn/scikit-learn/issues/28994')
        self.assertEqual(issues[0].creator, 'jeremycg')
        self.assertEqual(issues[0].labels, ["Documentation"])
        self.assertEqual(issues[0].state, State.open)
        self.assertEqual(issues[0].assignees, [])
        self.assertEqual(issues[0].title, "StratifiedShuffleSplit requires three copies of a lower class, rather than 2")
        self.assertEqual(issues[0].text, "Sample issue text...")
        self.assertEqual(issues[0].number, 28994)
        self.assertIsNotNone(issues[0].created_date)
        self.assertIsNotNone(issues[0].updated_date)
        self.assertEqual(issues[0].timeline_url, 'https://api.github.com/repos/scikit-learn/scikit-learn/issues/28994/timeline')
        self.assertEqual(len(issues[0].events), 1)
        self.assertEqual(issues[0].events[0].event_type, 'labeled')
        self.assertEqual(issues[0].events[0].author, 'jeremycg')
        self.assertIsNotNone(issues[0].events[0].event_date)
        self.assertEqual(issues[0].events[0].label, 'Bug')

    @patch('data_loader.config')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_issues_singleton(self, mock_file, mock_config):
        # Reset _ISSUES
        import data_loader
        data_loader._ISSUES = None

        mock_config.get_parameter.return_value = 'fake_path.json'
        sample_issues = []

        mock_file.return_value.read.return_value = json.dumps(sample_issues)

        loader = DataLoader()
        issues_first_call = loader.get_issues()
        issues_second_call = loader.get_issues()
        self.assertIs(issues_first_call, issues_second_call)  # Should be the same object due to singleton

    @patch('data_loader.config')
    @patch('builtins.open', side_effect=FileNotFoundError())
    def test_load_issues_file_not_found(self, mock_open_func, mock_config):
        mock_config.get_parameter.return_value = 'non_existent_file.json'
        loader = DataLoader()
        with self.assertRaises(FileNotFoundError):
            loader.get_issues()

    @patch('data_loader.config')
    @patch('builtins.open', new_callable=mock_open, read_data='Invalid JSON')
    def test_load_issues_invalid_json(self, mock_file, mock_config):
        mock_config.get_parameter.return_value = 'fake_path.json'
        mock_file.return_value.read.return_value = 'Invalid JSON'

        loader = DataLoader()
        with self.assertRaises(json.JSONDecodeError):
            loader.get_issues()

if __name__ == '__main__':
    unittest.main()
