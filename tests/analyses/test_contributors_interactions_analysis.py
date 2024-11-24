import unittest
from unittest.mock import patch, MagicMock
from argparse import Namespace
import networkx as nx
from analyses.contributors_interactions_analysis import ContributorsInteractionsAnalysis
from models.Issue import Issue
from models.State import State  # Assuming State enum is defined

class TestContributorsInteractionsAnalysis(unittest.TestCase):

    def setUp(self):
        self.analysis = ContributorsInteractionsAnalysis()

    @patch('data_loader.DataLoader.get_issues')
    def test_run(self, mock_get_issues):
        mock_issues = [
            Issue({
                "url": "https://github.com/scikit-learn/scikit-learn/issues/28994",
                "creator": "user1",
                "labels": ["Bug", "Documentation"],
                "state": "open",
                "assignees": [],
                "title": "Sample Issue",
                "text": "Sample issue text...",
                "number": 28994,
                "created_date": "2024-05-10T18:38:17+00:00",
                "updated_date": "2024-06-16T18:27:00+00:00",
                "timeline_url": "https://api.github.com/repos/scikit-learn/scikit-learn/issues/28994/timeline",
                "events": [
                    {
                        "event_type": "reopened",
                        "author": "user2",
                        "event_date": "2024-05-10T18:38:18+00:00",
                        "label": "Bug",
                        "comment": "Sample comment"
                    },
                    {
                        "event_type": "reopened",
                        "author": "user3",
                        "event_date": "2024-06-10T18:38:18+00:00",
                        "label": "Bug",
                        "comment": "Sample comment"
                    }
                ]
            })
        ]
        mock_get_issues.return_value = mock_issues

        args = Namespace(label=None, user=None)
        with patch.object(self.analysis, '_ContributorsInteractionsAnalysis__visualize_results') as mock_visualize:
            self.analysis.run(args)

            # Assert that the visualization method was called
            mock_visualize.assert_called_once()
            graph = mock_visualize.call_args[0][0]
            self.assertIsInstance(graph, nx.Graph)
            self.assertEqual(graph.number_of_nodes(), 3)
            self.assertEqual(graph.number_of_edges(), 3)  # Fully connected

    def test_analyze_network(self):
        graph = nx.Graph()
        graph.add_edge("user1", "user2", weight=2)
        graph.add_edge("user2", "user3", weight=1)

        degree_centrality, top_contributors = self.analysis._ContributorsInteractionsAnalysis__analyze_network(graph)

        # Check degree centrality calculation
        self.assertEqual(len(degree_centrality), 3)
        self.assertIn("user1", degree_centrality)
        self.assertIn("user2", degree_centrality)

        # Check top contributors
        self.assertEqual(len(top_contributors), 3)
        self.assertEqual(top_contributors[0][0], "user2")  # user2 has the highest centrality

    def test_create_graph(self):
        mock_issues = [
            Issue({
                "url": "https://github.com/scikit-learn/scikit-learn/issues/28994",
                "creator": "user1",
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
                        "author": "user2",
                        "event_date": "2024-05-10T18:38:18+00:00",
                        "label": "Bug",
                        "comment": "Sample comment"
                    },
                    {
                        "event_type": "reopened",
                        "author": "user3",
                        "event_date": "2024-05-10T18:38:18+00:00",
                        "label": "Bug",
                        "comment": "Sample comment"
                    }
                ]
            }),
            Issue({
                "url": "https://github.com/scikit-learn/scikit-learn/issues/28994",
                "creator": "user2",
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
                        "author": "user1",
                        "event_date": "2024-05-10T18:38:18+00:00",
                        "label": "Bug",
                        "comment": "Sample comment"
                    }
                ]
            }),
        ]

        graph = self.analysis._ContributorsInteractionsAnalysis__create_graph(mock_issues, None, None)

        # Check the graph properties
        self.assertIsInstance(graph, nx.Graph)
        self.assertEqual(graph.number_of_nodes(), 3)
        self.assertEqual(graph.number_of_edges(), 3)

        # Check graph structure
        self.assertTrue(graph.has_edge("user1", "user2"))
        self.assertTrue(graph.has_edge("user1", "user3"))

    @patch('sys.exit')  # Mock sys.exit to prevent it from terminating the test
    def test_create_graph_with_filters(self, mock_exit):
        mock_issues = [
            Issue({
                "url": "https://github.com/scikit-learn/scikit-learn/issues/28994",
                "creator": "user1",
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
                        "author": "user2",
                        "event_date": "2024-05-10T18:38:18+00:00",
                        "label": "Bug",
                        "comment": "Sample comment"
                    },
                    {
                        "event_type": "reopened",
                        "author": "user3",
                        "event_date": "2024-05-10T18:38:18+00:00",
                        "label": "Bug",
                        "comment": "Sample comment"
                    }
                ]
            }),
            Issue({
                "url": "https://github.com/scikit-learn/scikit-learn/issues/28994",
                "creator": "user4",
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
                        "author": "user5",
                        "event_date": "2024-05-10T18:38:18+00:00",
                        "label": "Bug",
                        "comment": "Sample comment"
                    }
                ]
            })
        ]

        # Test with label filter
        print("Test with label filter")
        graph = self.analysis._ContributorsInteractionsAnalysis__create_graph(mock_issues, "bug", None)
        self.assertEqual(graph.number_of_nodes(), 3)  # Only the first issue's participants
        self.assertTrue(graph.has_edge("user1", "user2"))

        # Test with user filter
        print("Test with user filter")
        graph = self.analysis._ContributorsInteractionsAnalysis__create_graph(mock_issues, None, "user4")
        self.assertEqual(graph.number_of_nodes(), 2)  # Only the second issue's participants
        self.assertTrue(graph.has_edge("user4", "user5"))

        mock_exit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
