from django.test import TestCase
import tempfile
from django.contrib.auth import get_user_model
from banners.models import *
from django.test import override_settings
from django.core.files import File


class QueueItemModel(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', phone_number='+375293969579')

        self.banner = Banner.objects.create(
            upload=File(tempfile.NamedTemporaryFile(suffix='.pdf')),
            user=user,
            phone_number='+375293969579'
        )
        self.queue_item1 = self.banner.queue.create(phone_number='+375445677421')
        self.queue_item2 = self.banner.queue.create(phone_number='+375445677422')

    def test_items_order_is_correct_on_queue_extension(self):
        self.assertEqual(self.queue_item1.position, 0)
        self.assertEqual(self.queue_item2.position, 1)
        self.assertEqual(self.banner.queue.first(), self.queue_item1)

    def test_items_order_is_correct_on_queue_reduction(self):
        self.banner.queue.first().delete()
        self.queue_item2.refresh_from_db()
        self.assertEqual(self.queue_item2.position, 0)
        self.assertEqual(self.banner.queue.first(), self.queue_item2)
