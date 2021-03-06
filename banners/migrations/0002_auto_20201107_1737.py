# Generated by Django 3.0.6 on 2020-11-07 17:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='preview',
            field=models.ImageField(null=True, upload_to='banner_previews/'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='upload',
            field=models.FileField(upload_to='banners/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
