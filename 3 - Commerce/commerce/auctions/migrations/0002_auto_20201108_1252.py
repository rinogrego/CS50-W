# Generated by Django 3.0.8 on 2020-11-08 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='description',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='latest_bidder',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='status',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='winner',
        ),
    ]