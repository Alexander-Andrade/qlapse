from django.test import TestCase
from datetime import timedelta
from banners.templatetags.queue_filters import time_passed_since_formatter
from django.utils import timezone


class TestTimePassedSinceFormatter(TestCase):
    def test_days(self):
        formatted_delta = time_passed_since_formatter(
            timezone.now() - timedelta(days=5)
        )

        self.assertEqual(formatted_delta, '5d')

    def test_days_and_hours(self):
        formatted_delta = time_passed_since_formatter(
            timezone.now() - timedelta(days=5, hours=5)
        )

        self.assertEqual(formatted_delta, '5d 5h')

    def test_days_hours_minutes(self):
        formatted_delta = time_passed_since_formatter(
            timezone.now() - timedelta(days=5, hours=5, minutes=5)
        )

        self.assertEqual(formatted_delta, '5d 5h')

    def test_days_hours_minutes_seconds(self):
        formatted_delta = time_passed_since_formatter(
            timezone.now() - timedelta(days=5, hours=5, minutes=12, seconds=12)
        )

        self.assertEqual(formatted_delta, '5d 5h')

    def test_minutes_seconds(self):
        formatted_delta = time_passed_since_formatter(
            timezone.now() - timedelta(minutes=12, seconds=12)
        )

        self.assertEqual(formatted_delta, '12m')

    def test_zero_time_passed(self):
        formatted_delta = time_passed_since_formatter(timezone.now())

        self.assertEqual(formatted_delta, 'few seconds ago')
