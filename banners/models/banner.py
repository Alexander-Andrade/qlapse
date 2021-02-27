from django.db import models
from django.core.validators import FileExtensionValidator
from shared.validators.phone_validator import phone_regex_validator
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser


class Banner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(_('phone'), validators=[phone_regex_validator],
                                    max_length=17)
    upload = models.FileField(upload_to='banners/', validators=[
        FileExtensionValidator(allowed_extensions=['pdf'])], null=True)
    preview = models.ImageField(upload_to='banner_previews/', null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number
