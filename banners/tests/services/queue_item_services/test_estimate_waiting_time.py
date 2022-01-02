from django.test import TestCase
from datetime import timedelta

from banners.services.queue_item_services.waiting_time.estimate_waiting_time import EstimateWaitingTime
from banners.tests.factories.banners import BannerFactory
from banners.tests.factories.queue_items import QueueItemFactory, QueueItemProcessedFactory


class EstimateWaitingTimeTest(TestCase):
    def setUp(self):
        self.banner = BannerFactory()

    def test_no_queue(self):
        QueueItemProcessedFactory(banner=self.banner)
        estimation = EstimateWaitingTime(banner=self.banner).call()

        self.assertEqual(estimation, timedelta(0))

    def test_no_processing_history(self):
        QueueItemFactory(banner=self.banner)
        estimation = EstimateWaitingTime(banner=self.banner).call()

        self.assertEqual(estimation, None)

    def test_estimation_for_the_whole_queue(self):
        QueueItemProcessedFactory(banner=self.banner,
                                  waiting_time_estimation=timedelta(minutes=5))
        QueueItemFactory(banner=self.banner)
        QueueItemFactory(banner=self.banner)
        estimation = EstimateWaitingTime(banner=self.banner).call()

        self.assertEqual(estimation, timedelta(minutes=10))

    def test_estimation_for_the_queue_item(self):
        QueueItemProcessedFactory(banner=self.banner,
                                  waiting_time_estimation=timedelta(minutes=5))
        queue_item1 = QueueItemFactory(banner=self.banner)
        queue_item2 = QueueItemFactory(banner=self.banner)
        estimation = EstimateWaitingTime(banner=self.banner,
                                         queue_item=queue_item2).call()

        self.assertEqual(estimation, timedelta(minutes=5))

    def test_estimation_for_the_queue_item_in_the_middle(self):
        QueueItemProcessedFactory(banner=self.banner,
                                  waiting_time_estimation=timedelta(minutes=12))
        QueueItemProcessedFactory(banner=self.banner,
                                  waiting_time_estimation=timedelta(minutes=5))
        queue_item1 = QueueItemFactory(banner=self.banner)
        queue_item2 = QueueItemFactory(banner=self.banner)
        queue_item3 = QueueItemFactory(banner=self.banner)
        estimation = EstimateWaitingTime(banner=self.banner,
                                         queue_item=queue_item2).call()

        self.assertEqual(estimation, timedelta(minutes=5))
