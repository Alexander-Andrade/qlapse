from banners.models import Banner
from django.core.files.base import ContentFile
from .pdf_banner_generator import PdfBannerGenerator
from .buy_twilio_number import BuyTwilioNumber
from shared.services.result import Success, Failure


class BannerCreator:

    def __init__(self, user):
        self.user = user

    def create(self):
        buy_number_result = BuyTwilioNumber().buy()

        if buy_number_result.failed:
            return buy_number_result

        banner_upload = PdfBannerGenerator(phone_number=buy_number_result.result).generate()

        banner = Banner(
            upload=ContentFile(banner_upload, name='%s.pdf'%(buy_number_result.result,)),
            phone_number=buy_number_result.result,
            user=self.user
        )

        banner.save()
        return Success(banner)
