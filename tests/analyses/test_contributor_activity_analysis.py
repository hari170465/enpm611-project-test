import unittest
from unittest.mock import MagicMock, patch
from analyses.contributor_activity_analysis import ContributorActivityAnalysis
from models.Issue import Issue
from models.Event import Event
from data_loader import DataLoader
import pandas as pd


# Mock Event and Issue classes
class Event:
    def __init__(self, author: str, event_date: str):
        self.author = author
        self.event_date = event_date


class Issue:
    def __init__(self, events: list):
        self.events = events


class TestContributorActivityAnalysis(unittest.TestCase):
    def setUp(self):
        # Mock data for issues and events
        self.issues = [
            Issue(events=[
                Event(author="user1", event_date="2024-01-01"),
                Event(author="user1", event_date="2024-02-01"),
                Event(author="user2", event_date="2024-01-15"),
            ]),
            Issue(events=[
                Event(author="user2", event_date="2024-03-01"),
                Event(author="user3", event_date="2024-01-20"),
            ]),
        ]

        # Mock DataLoader to return the mock issues
        DataLoader.get_issues = MagicMock(return_value=self.issues)

        # Instance of ContributorActivityAnalysis for testing
        self.analysis = ContributorActivityAnalysis()

    def test_create_dataframe(self):
        # Test the creation of the dataframe
        df = self.analysis._ContributorActivityAnalysis__create_dataframe(self.issues, user_filter=None)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)  # Total events
        self.assertTrue("author" in df.columns)
        self.assertTrue("event_date" in df.columns)

    def test_create_dataframe_with_user_filter(self):
        # Test the creation of the dataframe with a user filter
        df = self.analysis._ContributorActivityAnalysis__create_dataframe(self.issues, user_filter="user1")
        self.assertEqual(len(df), 2)  # Only events by 'user1'

    def test_aggregate(self):
        # Test the aggregation of events per user and month
        df = self.analysis._ContributorActivityAnalysis__create_dataframe(self.issues, user_filter=None)
        aggregated = self.analysis._ContributorActivityAnalysis__aggregate(df)
        self.assertIsInstance(aggregated, pd.DataFrame)
        self.assertTrue("author" in aggregated.columns)
        self.assertTrue("event_date" in aggregated.columns)
        self.assertTrue("event_count" in aggregated.columns)

        # Validate specific aggregation results
        user1_data = aggregated[(aggregated["author"] == "user1")]
        self.assertEqual(user1_data["event_count"].sum(), 2)

    @patch("matplotlib.pyplot.show")
    def test_visualize_results(self, mock_show):
        # Test visualization without displaying the plot
        df = self.analysis._ContributorActivityAnalysis__create_dataframe(self.issues, user_filter=None)
        aggregated = self.analysis._ContributorActivityAnalysis__aggregate(df)
        self.analysis._ContributorActivityAnalysis__visualize_results(df, aggregated)
        mock_show.assert_called_once()

    @patch("matplotlib.pyplot.show")
    def test_run(self, mock_show):
        # Test the run method with and without a user filter
        args = MagicMock()
        args.user = None
        self.analysis.run(args)

        args.user = "user1"
        self.analysis.run(args)
        mock_show.assert_called()


if __name__ == "__main__":
    unittest.main()

