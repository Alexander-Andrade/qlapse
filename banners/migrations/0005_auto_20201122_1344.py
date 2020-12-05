# Generated by Django 3.0.6 on 2020-11-22 13:44

import banners.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0004_auto_20201122_1239'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='queueitem',
            options={'ordering': ('position',)},
        ),
        migrations.AlterField(
            model_name='queueitem',
            name='status',
            field=models.IntegerField(choices=[(1, 'QUEUE'), (2, 'PROCESSING'), (3, 'PROCESSED'), (4, 'SKIPPED')], default=banners.models.QueueItemStatus['QUEUE']),
        ),
    ]