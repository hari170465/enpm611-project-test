import unittest
from unittest.mock import MagicMock, patch
from analyses.active_labels_analysis import ActiveLabelsAnalysis
from models.Issue import Issue
from models.Event import Event
from data_loader import DataLoader
import pandas as pd


# Mock Event and Issue classes for compatibility
class Event:
    def __init__(self, event_type: str):
        self.event_type = event_type


class Issue:
    def __init__(self, labels: list, events: list):
        self.labels = labels
        self.events = events


class TestActiveLabelsAnalysis(unittest.TestCase):
    def setUp(self):
        # Mock issues data
        self.issues = [
            Issue(
                labels=["bug", "feature"],
                events=[
                    Event(event_type="commented"),
                    Event(event_type="commented"),
                    Event(event_type="closed"),
                ],
            ),
            Issue(
                labels=["documentation", "feature"],
                events=[
                    Event(event_type="commented"),
                ],
            ),
            Issue(
                labels=["bug"],
                events=[
                    Event(event_type="commented"),
                ],
            ),
        ]

        # Mock DataLoader to return the mock issues
        DataLoader.get_issues = MagicMock(return_value=self.issues)

        # Instance of ActiveLabelsAnalysis for testing
        self.analysis = ActiveLabelsAnalysis()

    def test_create_dataframe(self):
        # Test the creation of the dataframe
        df = self.analysis._ActiveLabelsAnalysis__create_dataframe(self.issues, label_filter=None)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)  # Total rows = total label occurrences
        self.assertTrue("label" in df.columns)
        self.assertTrue("num_comments" in df.columns)

    def test_aggregate(self):
        # Test the aggregation of comments per label
        df = self.analysis._ActiveLabelsAnalysis__create_dataframe(self.issues, label_filter=None)
        aggregated = self.analysis._ActiveLabelsAnalysis__aggregate(df)
        self.assertEqual(aggregated["bug"], 3)  # 'bug' has 3 comments total
        self.assertEqual(aggregated["feature"], 3)  # 'feature' has 3 comments total
        self.assertEqual(aggregated["documentation"], 1)  # 'documentation' has 1 comment total

    def test_print_occurrences(self):
        # Test the printing of label occurrences
        with patch("builtins.print") as mocked_print:
            self.analysis._ActiveLabelsAnalysis__print_occurrences(self.issues, "bug")
            mocked_print.assert_called_with("\n\nThe label 'bug' occurred 2 times across 3 issues.\n")

    def test_visualize_results(self):
        # Test visualization without displaying the plot
        df = self.analysis._ActiveLabelsAnalysis__create_dataframe(self.issues, label_filter=None)
        aggregated = self.analysis._ActiveLabelsAnalysis__aggregate(df)

        with patch("matplotlib.pyplot.show"):
            self.analysis._ActiveLabelsAnalysis__visualize_results(aggregated, top_n=2, label_filter=None)

    def test_run_with_label_filter(self):
        # Test the run method with a label filter
        with patch("matplotlib.pyplot.show"):
            args = MagicMock()
            args.label = "bug"
            args.active_labels = 2
            self.analysis.run(args)

    def test_run_without_label_filter(self):
        # Test the run method without a label filter
        with patch("matplotlib.pyplot.show"):
            args = MagicMock()
            args.label = None
            args.active_labels = 2
            self.analysis.run(args)


if __name__ == "__main__":
    unittest.main()

