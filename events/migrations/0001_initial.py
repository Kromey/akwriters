# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('remote_id', models.CharField(max_length=60)),
                ('css_class', models.CharField(max_length=10)),
            ],
        ),
    ]