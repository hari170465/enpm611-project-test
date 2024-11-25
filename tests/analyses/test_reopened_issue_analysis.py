import unittest
from unittest.mock import patch
import pandas as pd
from analyses.reopened_issue_analysis import ReopenedIssueAnalysis
from argparse import Namespace
from models.Issue import Issue
# from models.Event import Event
# import sys

class TestReopenedIssueAnalysis(unittest.TestCase):

    def setUp(self):
        # Initialize the analysis class
        self.analysis = ReopenedIssueAnalysis()

    @patch('data_loader.DataLoader.get_issues')
    @patch('analyses.reopened_issue_analysis.ReopenedIssueAnalysis._ReopenedIssueAnalysis__visualize_results')
    def test_run(self, mock_visualize_results, mock_get_issues):
        # Mock data returned by DataLoader
        mock_issues = [
            Issue({
                "url": "https://github.com/scikit-learn/scikit-learn/issues/28994",
                "creator": "jeremycg",
                "labels": ["Bug", "Documentation"],
                "state": "open",
                "assignees": [],
                "title": "Sample Issue",
                "text": "Sample issue text...",
                "number": 28994,
                "created_date": "2024-05-10T18:38:17+00:00",
                "updated_date": "2024-05-16T18:27:00+00:00",
                "timeline_url": "https://api.github.com/repos/scikit-learn/scikit-learn/issues/28994/timeline",
                "events": [
                    {
                        "event_type": "reopened",
                        "author": "jeremycg",
                        "event_date": "2024-05-10T18:38:18+00:00",
                        "label": "Bug",
                        "comment": "Sample comment"
                    }
                ]
            })
        ]
        mock_get_issues.return_value = mock_issues

        # Mock the arguments
        args = Namespace(labels=5)

        # Call the run method
        self.analysis.run(args)

        # Verify visualization was called
        mock_visualize_results.assert_called_once()
    @patch('data_loader.DataLoader.get_issues')
    def test_create_dataframe(self, mock_get_issues):
        mock_issues = [
            Issue({
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
                        "event_type": "reopened",
                        "author": "jeremycg",
                        "event_date": "2024-05-10T18:38:18+00:00",
                        "label": "Bug",
                        "comment": "Sample comment"
                    }
                ]
            })
            
        ]
        mock_get_issues.return_value = mock_issues

        df = self.analysis._ReopenedIssueAnalysis__create_dataframe(mock_issues)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)

    def test_empty_dataframe(self):
        # Mock empty issue data
        mock_issues = []

        # Test that SystemExit is raised when an empty dataframe is processed
        with self.assertRaises(SystemExit):
            df = self.analysis._ReopenedIssueAnalysis__create_dataframe(mock_issues)

    def test_empty_aggregation(self):
        # Mock empty dataframe
        mock_df = pd.DataFrame(columns=['labels', 'reopen_count'])

        # Run the private method to test aggregation
        aggregated = self.analysis._ReopenedIssueAnalysis__aggregate(mock_df, number_of_labels=2)
        self.assertTrue(aggregated.empty)

if __name__ == '__main__':
    unittest.main()
