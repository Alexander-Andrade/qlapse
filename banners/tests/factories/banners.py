import factory
from faker import Factory
from banners.models import Banner
from accounts.tests.factories.users import UserFactory
from django.core.files import File
from accounts.tests.factories.fake_number_provider import CustomPhoneProvider


faker = Factory.create()
faker.add_provider(CustomPhoneProvider)


class BannerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Banner

    upload = factory.LazyAttribute(
        lambda _: File(open("media/testfiles/banners/12057511042.pdf", encoding="ISO8859-1")))
    user = factory.SubFactory(UserFactory)
    phone_number = factory.LazyAttribute(lambda user: faker.phone_number())
