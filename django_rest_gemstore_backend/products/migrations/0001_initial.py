# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GemProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('canPurchase', models.BooleanField()),
                ('images', models.ImageField(upload_to='', verbose_name='Upload Gem Photo')),
            ],
        ),
    ]
