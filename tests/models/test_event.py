import unittest
from models.Event import Event

class TestEvent(unittest.TestCase):
    def test_event_full_data(self):
        jobj = {
            'event_type': 'commented',
            'author': 'test_user',
            'event_date': '2024-01-01T00:00:00Z',
            'label': 'bug',
            'comment': 'This is a test comment.'
        }
        event = Event(jobj)
        self.assertEqual(event.event_type, 'commented')
        self.assertEqual(event.author, 'test_user')
        self.assertIsNotNone(event.event_date)
        self.assertEqual(event.label, 'bug')
        self.assertEqual(event.comment, 'This is a test comment.')

    def test_event_partial_data(self):
        jobj = {
            'event_type': 'closed',
            'event_date': '2024-01-01T00:00:00Z',
        }
        event = Event(jobj)
        self.assertEqual(event.event_type, 'closed')
        self.assertIsNone(event.author)
        self.assertIsNotNone(event.event_date)
        self.assertIsNone(event.label)
        self.assertIsNone(event.comment)

    def test_event_invalid_date(self):
        jobj = {
            'event_date': 'invalid_date'
        }
        event = Event(jobj)
        self.assertIsNone(event.event_date)

    def test_event_no_data(self):
        event = Event(None)
        self.assertIsNone(event.event_type)
        self.assertIsNone(event.author)
        self.assertIsNone(event.event_date)
        self.assertIsNone(event.label)
        self.assertIsNone(event.comment)
