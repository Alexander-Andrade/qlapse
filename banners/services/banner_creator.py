from banners.models import Banner
from django.core.files.base import ContentFile
from .pdf_banner_generator import PdfBannerGenerator
from .buy_twilio_number import BuyTwilioNumber


class BannerCreator:

    def __init__(self, user):
        self.user = user

    def create(self):
        buy_number_result = BuyTwilioNumber().buy()

        if 'error' in buy_number_result:
            return buy_number_result

        banner_upload = PdfBannerGenerator(phone_number=buy_number_result['success']).generate()
        banner = Banner(upload=ContentFile(banner_upload, name='%s.pdf'%(buy_number_result['success'],)),
                        phone_number=buy_number_result['success'],
                        user=self.user)

        banner.save()
        return {'success': banner}
