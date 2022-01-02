import vcr

from django.test import TestCase
from banners.models import Banner
from accounts.tests.factories.users import UserFactory
from banners.services import BannerCreator


class BannerCreatorTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    @vcr.use_cassette('banners/tests/cassettes/banner_creator_create.yaml')
    def test_create(self):
        creation_result = BannerCreator(user=self.user).create()
        self.assertIsInstance(creation_result.result, Banner)

    def test_create_with_fake_number(self):
        with self.settings(FAKE_BANNER_PHONE_NUMBERS=True):
            creation_result = BannerCreator(user=self.user).create()
            self.assertIsInstance(creation_result.result, Banner)

