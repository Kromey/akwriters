# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-07 22:25
from __future__ import unicode_literals

from django.db import migrations
import forum.models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20171006_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=forum.models.MarkdownField(help_text='We use a slightly-customized version of <a data-toggle="modal" data-target="#MarkdownHelp">Markdown</a> for formatting.'),
        ),
    ]
