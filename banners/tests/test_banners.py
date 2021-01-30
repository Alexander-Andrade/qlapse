from django.test import TestCase
from ..services.banner_creator import BannerCreator
from django.contrib.auth import get_user_model
from banners.models import Banner
import vcr


class BannerCreatorTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.\
            create_user(email='test@gmail.com', phone_number="+375293969579", password='password')

    @vcr.use_cassette('banners/tests/cassettes/banner_creator_create.yaml')
    def test_create(self):
        creation_result = BannerCreator(user=self.user).create()
        self.assertIsInstance(creation_result.result, Banner)