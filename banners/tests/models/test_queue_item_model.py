from django.test import TestCase
from banners.tests.factories.banners import BannerFactory
from banners.tests.factories.queue_items import QueueItemFactory


class QueueItemModel(TestCase):
    def setUp(self):
        self.banner = BannerFactory()
        self.queue_item1 = QueueItemFactory(banner=self.banner)
        self.queue_item2 = QueueItemFactory(banner=self.banner)

    def test_items_order_is_correct_on_queue_extension(self):
        self.assertEqual(self.queue_item1.position, 0)
        self.assertEqual(self.queue_item2.position, 1)
        self.assertEqual(self.banner.queue.first(), self.queue_item1)

    def test_items_order_is_correct_on_queue_reduction(self):
        self.banner.queue.first().delete()
        self.queue_item2.refresh_from_db()
        self.assertEqual(self.queue_item2.position, 0)
        self.assertEqual(self.banner.queue.first(), self.queue_item2)

    def test_past_item_goes_to_the_end(self):
        queue_item3 = QueueItemFactory(banner=self.banner)
        self.queue_item1.past = True
        self.queue_item1.save()
        self.queue_item1.refresh_from_db()

        self.assertEqual(self.queue_item1.position, 0)
        self.assertEqual(self.banner.queue.past().first(), self.queue_item1)

        self.queue_item2.past = True
        self.queue_item2.save()
        self.queue_item2.refresh_from_db()

        self.assertEqual(self.queue_item2.position, 1)
        self.assertEqual(self.banner.queue.past().all()[1], self.queue_item2)

        queue_item3.past = True
        queue_item3.save()
        queue_item3.refresh_from_db()

        self.assertEqual(queue_item3.position, 2)
        self.assertEqual(self.banner.queue.past().last(), queue_item3)
