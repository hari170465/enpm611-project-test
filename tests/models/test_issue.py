import unittest
from models.Issue import Issue
from models.State import State

class TestIssue(unittest.TestCase):
    def test_issue_full_data(self):
        jobj = {
            'url': 'http://example.com/issue/1',
            'creator': 'test_user',
            'labels': ['bug', 'urgent'],
            'state': 'open',
            'assignees': ['assignee1', 'assignee2'],
            'title': 'Test Issue',
            'text': 'This is a test issue.',
            'number': '1',
            'created_date': '2024-01-01T00:00:00Z',
            'updated_date': '2024-01-02T00:00:00Z',
            'timeline_url': 'http://example.com/issue/1/timeline',
            'events': [{'event_type': 'created', 'author': 'test_user', 'event_date': '2024-01-01T00:00:00Z'}]
        }
        issue = Issue(jobj)
        self.assertEqual(issue.url, 'http://example.com/issue/1')
        self.assertEqual(issue.creator, 'test_user')
        self.assertEqual(issue.labels, ['bug', 'urgent'])
        self.assertEqual(issue.state, State.open)
        self.assertEqual(issue.assignees, ['assignee1', 'assignee2'])
        self.assertEqual(issue.title, 'Test Issue')
        self.assertEqual(issue.text, 'This is a test issue.')
        self.assertEqual(issue.number, 1)
        self.assertIsNotNone(issue.created_date)
        self.assertIsNotNone(issue.updated_date)
        self.assertEqual(issue.timeline_url, 'http://example.com/issue/1/timeline')
        self.assertEqual(len(issue.events), 1)

    def test_issue_partial_data(self):
        jobj = {
            'url': 'http://example.com/issue/1',
            'state': 'closed',
            'number': '2',
        }
        issue = Issue(jobj)
        self.assertEqual(issue.url, 'http://example.com/issue/1')
        self.assertIsNone(issue.creator)
        self.assertEqual(issue.labels, [])
        self.assertEqual(issue.state, State.closed)
        self.assertEqual(issue.assignees, [])
        self.assertIsNone(issue.title)
        self.assertIsNone(issue.text)
        self.assertEqual(issue.number, 2)
        self.assertIsNone(issue.created_date)
        self.assertIsNone(issue.updated_date)
        self.assertIsNone(issue.timeline_url)
        self.assertEqual(issue.events, [])

    def test_issue_invalid_number(self):
        jobj = {'number': 'invalid', 'state': 'open'}
        issue = Issue(jobj)
        self.assertEqual(issue.number, -1)
        self.assertEqual(issue.state, State.open)

    def test_issue_invalid_dates(self):
        jobj = {
            'created_date': 'invalid_date',
            'updated_date': 'another_bad_date',
            'state': 'closed'
        }
        issue = Issue(jobj)
        self.assertIsNone(issue.created_date)
        self.assertIsNone(issue.updated_date)
        self.assertEqual(issue.state, State.closed)

