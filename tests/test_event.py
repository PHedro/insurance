import unittest

from insurance.model import Event


class EventTestCase(unittest.TestCase):
    def test_correctly_initialized(self):
        result = Event(event_id=1, deal_id=2, loss=3000)

        self.assertEqual(1, result.event_id)
        self.assertEqual(2, result.deal_id)
        self.assertEqual(3000, result.loss)

    def test_raises_error_with_missing_event_id(self):
        with self.assertRaises(TypeError):
            Event(deal_id=2, loss=3000)

    def test_raises_error_with_missing_deal_id(self):
        with self.assertRaises(TypeError):
            Event(event_id=1, loss=3000)

    def test_raises_error_with_missing_loss(self):
        with self.assertRaises(TypeError):
            Event(event_id=1, deal_id=2)
