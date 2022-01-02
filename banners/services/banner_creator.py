from banners.models import Banner
from django.core.files.base import ContentFile

from .buy_or_fake_phone_number import BuyOrFakePhoneNumber
from .pdf_banner_generator import PdfBannerGenerator
from shared.services.result import Success, Failure
from django.db import transaction


class BannerCreator:

    def __init__(self, user):
        self.user = user

    @transaction.atomic
    def create(self):
        phone_number_result = BuyOrFakePhoneNumber().call()
        if phone_number_result.failed:
            return phone_number_result

        phone_number = phone_number_result.result

        banner = Banner(
            phone_number=phone_number,
            user=self.user
        )
        banner.save()
        banner_upload = PdfBannerGenerator(
            banner=banner
        ).generate()
        banner.upload = ContentFile(banner_upload,
                                    name='%s.pdf'%(phone_number,))
        banner.save()
        return Success(banner)
