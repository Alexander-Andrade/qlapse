# Generated by Django 3.0.6 on 2020-12-06 19:16

import banners.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0005_auto_20201122_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queueitem',
            name='status',
            field=models.IntegerField(choices=[(1, 'QUEUED'), (2, 'PROCESSING')], default=banners.models.QueueItemStatus['QUEUED']),
        ),
    ]
