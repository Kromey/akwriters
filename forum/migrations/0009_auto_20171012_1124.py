# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-12 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_migrate_ops'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='topic',
        ),
        migrations.AlterField(
            model_name='post',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='forum.Board'),
        ),
    ]
