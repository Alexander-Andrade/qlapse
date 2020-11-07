from django.test import TestCase
from .services.banner_creator import BannerCreator
from accounts.models import CustomUser
from banners.models import Banner
import vcr


class BannerCreatorTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.\
            create_user(email='test@gmail.com', phone_number="+375293969579", password='password')

    @vcr.use_cassette('banners/cassettes/banner_creator_create.yaml')
    def test_create(self):
        creation_result = BannerCreator(user=self.user).create()
        self.assertIsInstance(creation_result.result, Banner)


        



