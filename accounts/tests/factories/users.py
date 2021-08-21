import factory
from faker import Factory
from django.contrib.auth import get_user_model
from accounts.tests.factories.fake_number_provider import CustomPhoneProvider

faker = Factory.create()
faker.add_provider(CustomPhoneProvider)
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda user: faker.email())
    username = factory.LazyAttribute(lambda _: faker.word())
    password = factory.LazyAttribute(lambda _: faker.word())
    phone_number = factory.LazyAttribute(lambda user: faker.phone_number())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = model_class(*args, **kwargs)
        user.set_password(user.password)
        user.save()
        return user
