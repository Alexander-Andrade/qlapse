from django.test import TestCase
import tempfile
from django.test import override_settings
from banners.tests.factories.banners import BannerFactory
from banners.tests.factories.queue_items import QueueItemFactory


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
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
