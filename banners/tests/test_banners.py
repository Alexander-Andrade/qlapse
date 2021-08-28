from django.test import TestCase, Client

from accounts.tests.factories.users import UserFactory
from .factories.banners import BannerFactory
from ..services.banner_creator import BannerCreator
from banners.views import create
from banners.models import Banner
import vcr
from django.test.client import RequestFactory
from django.urls import reverse


class BannerCreatorTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    @vcr.use_cassette('banners/tests/cassettes/banner_creator_create.yaml')
    def test_create(self):
        creation_result = BannerCreator(user=self.user).create()
        self.assertIsInstance(creation_result.result, Banner)

    def test_create_with_fake_number(self):
        creation_result = BannerCreator(user=self.user, fake_banner_number=True).\
            create()
        self.assertIsInstance(creation_result.result, Banner)


class CreateViewTest(TestCase):
    def setUp(self):
        self.banner = BannerFactory()

        self.request_factory = RequestFactory()
        self.request = self.request_factory.post(reverse("banners:create"))
        self.request.user = self.banner.user

    @vcr.use_cassette('banners/tests/cassettes/banner_creator_create.yaml')
    def test_create_redirects_to_banners_list(self):
        response = create(self.request)
        response.client = Client()

        self.assertRedirects(
            response,
            reverse('banners:index'),
            target_status_code=302
        )
