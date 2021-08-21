# Generated by Django 3.0.6 on 2021-02-21 18:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0009_bannertelegram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='upload',
            field=models.FileField(null=True, upload_to='banners/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
