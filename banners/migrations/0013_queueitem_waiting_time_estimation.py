# Generated by Django 3.1.12 on 2021-08-30 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0012_auto_20210828_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='queueitem',
            name='waiting_time_estimation',
            field=models.DurationField(null=True),
        ),
    ]
