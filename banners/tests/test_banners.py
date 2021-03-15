from django.test import TestCase, Client
from ..services.banner_creator import BannerCreator
from banners.views import create
from django.contrib.auth import get_user_model
from banners.models import Banner
import vcr
from django.test import override_settings
import tempfile
from django.test.client import RequestFactory
from django.urls import reverse
from django.core.files import File

User = get_user_model()


class BannerCreatorTest(TestCase):
    def setUp(self):
        self.user = User.objects.\
            create_user(email='test@gmail.com', phone_number="+375293969579", password='password')

    @vcr.use_cassette('banners/tests/cassettes/banner_creator_create.yaml')
    def test_create(self):
        creation_result = BannerCreator(user=self.user).create()
        self.assertIsInstance(creation_result.result, Banner)

    def test_create_with_fake_number(self):
        creation_result = BannerCreator(user=self.user, fake_banner_number=True).\
            create()
        self.assertIsInstance(creation_result.result, Banner)


class CreateViewTest(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        user = User.objects.create_user(
            email='normal@user.com',
            password='foo',
            phone_number='+375293969579')

        self.banner = Banner.objects.create(
            upload=File(tempfile.NamedTemporaryFile(suffix='.pdf')),
            user=user,
            phone_number='+375293969579'
        )

        self.request_factory = RequestFactory()
        self.request = self.request_factory.post(reverse("banners:create"))
        self.request.user = user

    @vcr.use_cassette('banners/tests/cassettes/banner_creator_create.yaml')
    def test_create_redirects_to_banners_list(self):
        response = create(self.request)
        response.client = Client()

        self.assertRedirects(
            response,
            reverse('banners:index'),
            target_status_code=302
        )
