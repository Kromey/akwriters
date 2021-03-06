# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-03 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import passwordless.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=passwordless.utils.make_token, max_length=40, unique=True)),
                ('session_key', models.CharField(default=passwordless.utils.make_token, max_length=40)),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_expires', models.DateTimeField(default=passwordless.utils.expiration_date)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='authtoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passwordless.User'),
        ),
    ]
