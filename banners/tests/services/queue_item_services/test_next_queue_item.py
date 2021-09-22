from django.test import TestCase
from unittest.mock import patch
from datetime import timedelta
from django.utils import timezone
import time_machine

from banners.models import QueueItemStatus
from banners.services import NextQueueItem
from banners.tests.factories.banners import BannerFactory
from banners.tests.factories.queue_items import QueueItemProcessingFactory, QueueItemProcessedFactory, QueueItemFactory


class NextQueueItemTest(TestCase):
    def setUp(self):
        self.banner = BannerFactory()

    @patch('twilio.rest.Client.messages')
    def test_processed_item_fields(self, twilio_client_class):
        queue_item = QueueItemProcessingFactory(banner=self.banner)
        NextQueueItem(banner=self.banner).next()

        queue_item.refresh_from_db()

        self.assertEqual(queue_item.past, True)
        self.assertEqual(queue_item.status, QueueItemStatus.PROCESSED)
        self.assertIsNotNone(queue_item.processing_ended_at)

    @patch('twilio.rest.Client.messages')
    def test_no_new_items(self, twilio_client_class):
        QueueItemProcessedFactory(banner=self.banner)
        new_queue_item = NextQueueItem(banner=self.banner).next()

        self.assertIs(new_queue_item.result, None)

    @patch('twilio.rest.Client.messages')
    def test_next_item_fields(self, twilio_client_class):
        queue_item = QueueItemFactory(banner=self.banner)
        NextQueueItem(banner=self.banner).next()

        queue_item.refresh_from_db()

        self.assertEqual(queue_item.status, QueueItemStatus.PROCESSING)
        self.assertIsNone(queue_item.waiting_time_estimation)
        self.assertIsNotNone(queue_item.processing_started_at)

    @patch('twilio.rest.Client.messages')
    def test_estimation_when_no_processed_items(self, twilio_client_class):
        queue_item = QueueItemFactory(banner=self.banner)
        NextQueueItem(banner=self.banner).next()

        queue_item.refresh_from_db()

        self.assertIsNone(queue_item.waiting_time_estimation)

    @patch('twilio.rest.Client.messages')
    def test_estimations(self, twilio_client_class):
        # first person got to the queue
        traveller = time_machine.travel(timezone.now() - timedelta(minutes=30))
        traveller.start()
        queue_item = QueueItemFactory(banner=self.banner)
        traveller.stop()
        # first person processing
        traveller = time_machine.travel(timezone.now() - timedelta(minutes=25))
        traveller.start()
        NextQueueItem(banner=self.banner).next()
        traveller.stop()
        queue_item.refresh_from_db()

        self.assertIsNone(queue_item.waiting_time_estimation)

        # second person got to the queue
        traveller = time_machine.travel(timezone.now() - timedelta(minutes=24))
        traveller.start()
        queue_item2 = QueueItemFactory(banner=self.banner)
        traveller.stop()
        # first person processed
        # second one is in processing status
        traveller = time_machine.travel(timezone.now() - timedelta(minutes=23))
        traveller.start()
        NextQueueItem(banner=self.banner).next()
        traveller.stop()
        queue_item.refresh_from_db()
        queue_item2.refresh_from_db()

        # real processing period is written to the first person estimation
        self.assertEqual(
            queue_item.waiting_time_estimation,
            queue_item.processing_ended_at - queue_item.processing_started_at
        )

        # third person got to the queue
        traveller = time_machine.travel(timezone.now() - timedelta(minutes=21))
        traveller.start()
        queue_item3 = QueueItemFactory(banner=self.banner)
        traveller.stop()

        # second one is processed; third is in processing
        traveller = time_machine.travel(timezone.now() - timedelta(minutes=20))
        traveller.start()
        NextQueueItem(banner=self.banner).next()
        traveller.stop()
        queue_item2.refresh_from_db()
        queue_item3.refresh_from_db()

        # estimation is a convolution of the first processed and the second one
        self.assertEqual(
            queue_item2.waiting_time_estimation,
            ((queue_item.processing_ended_at - queue_item.processing_started_at)/2) +
            ((queue_item2.processing_ended_at - queue_item2.processing_started_at)/2)
        )

        # third one is processed
        traveller = time_machine.travel(timezone.now() - timedelta(minutes=16))
        traveller.start()
        NextQueueItem(banner=self.banner).next()
        traveller.stop()
        queue_item3.refresh_from_db()

        # estimation is a convolution of the first, second and third processed items
        self.assertEqual(
            queue_item3.waiting_time_estimation,
            (queue_item2.waiting_time_estimation / 2) +
            ((queue_item3.processing_ended_at - queue_item3.processing_started_at)/2)
        )

        # fourth person got to the queue
        traveller = time_machine.travel(timezone.now() - timedelta(minutes=12))
        traveller.start()
        queue_item4 = QueueItemFactory(banner=self.banner)
        traveller.stop()

        # fourth is in processing state
        traveller = time_machine.travel(timezone.now() - timedelta(minutes=9))
        traveller.start()
        NextQueueItem(banner=self.banner).next()
        traveller.stop()

        # fourth is processed
        traveller = time_machine.travel(timezone.now() - timedelta(minutes=8))
        traveller.start()
        NextQueueItem(banner=self.banner).next()
        traveller.stop()

        queue_item4.refresh_from_db()
        # estimation is a convolution of the first, second, third,
        # fourth processing times
        first_estimation = queue_item.processing_ended_at - queue_item.processing_started_at
        second_estimation = \
            (first_estimation/2) + \
            ((queue_item2.processing_ended_at - queue_item2.processing_started_at)/2)
        third_estimation = \
            (second_estimation / 2) + \
            ((queue_item3.processing_ended_at - queue_item3.processing_started_at) / 2)
        fourth_estimation = \
            (third_estimation / 2) + \
            ((queue_item4.processing_ended_at - queue_item4.processing_started_at) / 2)
        self.assertEqual(
            queue_item4.waiting_time_estimation,
            fourth_estimation
        )
