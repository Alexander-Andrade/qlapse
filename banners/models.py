from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser


class Banner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(_('phone'), validators=[phone_regex], max_length=17)
    upload = models.FileField(upload_to='banners/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    preview = models.ImageField(upload_to='banner_previews/', null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number