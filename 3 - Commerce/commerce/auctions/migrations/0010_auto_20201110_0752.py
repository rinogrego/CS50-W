# Generated by Django 3.0.8 on 2020-11-10 00:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201110_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='Watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]