# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passwordless', '0003_apppassword_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apppassword',
            options={'ordering': ['created_on']},
        ),
        migrations.AddField(
            model_name='user',
            name='jid_node',
            field=models.CharField(max_length=30, null=True),
        ),
    ]