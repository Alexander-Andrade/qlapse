from banners.models import Banner
from django.core.files.base import ContentFile
from .pdf_banner_generator import PdfBannerGenerator
from .buy_twilio_number import BuyTwilioNumber
from shared.services.result import Success, Failure
from django.db import transaction
from common.utils import fake_phone_number


class BannerCreator:

    def __init__(self, user, fake_banner_number=False):
        self.user = user
        self.fake_banner_number = fake_banner_number

    @transaction.atomic
    def create(self):
        phone_number = None

        if not self.fake_banner_number:
            buy_number_result = BuyTwilioNumber().buy()

            if buy_number_result.failed:
                return buy_number_result
            phone_number = buy_number_result.result
        else:
            phone_number = fake_phone_number()

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
