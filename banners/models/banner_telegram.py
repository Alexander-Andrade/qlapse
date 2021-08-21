from django.db import models
from django.core.validators import MinValueValidator


class BannerTelegram(models.Model):
    banner = models.ForeignKey('banners.Banner', on_delete=models.CASCADE)
    chat_id = models.BigIntegerField(null=True,
                                     validators=[MinValueValidator(0)])
