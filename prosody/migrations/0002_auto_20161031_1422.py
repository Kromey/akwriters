# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 22:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prosody', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProsodyRoster',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('prosody.prosody',),
        ),
        migrations.AlterModelOptions(
            name='prosody',
            options={'ordering': ['user', 'store', 'key']},
        ),
    ]
