import factory
from faker import Factory
from banners.models import BannerTelegram
from accounts.tests.factories.fake_number_provider import CustomPhoneProvider

faker = Factory.create()
faker.add_provider(CustomPhoneProvider)


class BannerTelegramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BannerTelegram
