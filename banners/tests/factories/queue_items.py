from django.utils import timezone
from datetime import timedelta

import factory
from faker import Factory
from banners.models import QueueItem, QueueItemSource, QueueItemStatus
from accounts.tests.factories.fake_number_provider import CustomPhoneProvider
from banners.tests.factories.banner_telegrams import BannerTelegramFactory
from banners.tests.factories.banners import BannerFactory
from faker import Faker

faker = Factory.create()
faker.add_provider(CustomPhoneProvider)
fake = Faker()


class QueueItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QueueItem

    banner = factory.SubFactory(BannerFactory)
    phone_number = factory.LazyAttribute(lambda _: faker.phone_number())


class QueueItemProcessingFactory(QueueItemFactory):
    status = QueueItemStatus.PROCESSING
    processing_started_at = factory.\
        LazyAttribute(lambda _: timezone.now() - timedelta(minutes=10))


class QueueItemProcessedFactory(QueueItemFactory):
    status = QueueItemStatus.PROCESSED
    past = True
    processing_started_at = factory.\
        LazyAttribute(lambda _: timezone.now() - timedelta(minutes=10))
    processing_ended_at = factory.\
        LazyAttribute(lambda queue_item: queue_item.processing_started_at + timedelta(minutes=5))


class QueueItemTelegramFactory(QueueItemFactory):
    source = QueueItemSource.TELEGRAM
    telegram_chat_id = factory.LazyAttribute(lambda _: fake.unique.random_int())

    @factory.post_generation
    def after_create(obj, create, extracted, **kwargs):
        BannerTelegramFactory(banner=obj.banner, chat_id=obj.telegram_chat_id)
