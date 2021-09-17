import vcr
from django.test.client import RequestFactory
from django.urls import reverse
from django.test import TestCase, Client

from .factories.banners import BannerFactory
from banners.views import create


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
