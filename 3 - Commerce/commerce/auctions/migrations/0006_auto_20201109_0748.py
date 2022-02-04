# Generated by Django 3.0.8 on 2020-11-09 00:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='name',
            new_name='title',
        ),
        migrations.CreateModel(
            name='ListingComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]