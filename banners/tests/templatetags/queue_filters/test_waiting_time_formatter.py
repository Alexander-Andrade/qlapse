from django.test import TestCase
from datetime import timedelta
from banners.templatetags.queue_filters import waiting_time_formatter


class TestWaitingTimeFormatter(TestCase):
    def test_days(self):
        formatted_time = waiting_time_formatter(timedelta(days=5))

        self.assertEqual(formatted_time, '120h')

    def test_days_and_hours(self):
        formatted_time = waiting_time_formatter(timedelta(days=5, hours=5))

        self.assertEqual(formatted_time, '125h')

    def test_days_and_hours_minutes(self):
        delta = timedelta(days=5, hours=5, minutes=5)
        formatted_time = waiting_time_formatter(delta)

        self.assertEqual(formatted_time, '125h 5m')

    def test_days_hours_minutes_seconds(self):
        delta = timedelta(days=5, hours=5, minutes=12, seconds=12)
        formatted_time = waiting_time_formatter(delta)

        self.assertEqual(formatted_time, '125h 12m')

    def test_minutes_seconds(self):
        delta = timedelta(minutes=12, seconds=12)
        formatted_time = waiting_time_formatter(delta)

        self.assertEqual(formatted_time, '12m 12s')

    def test_no_estimation(self):
        formatted_time = waiting_time_formatter(None)

        self.assertEqual(formatted_time, '∞')
