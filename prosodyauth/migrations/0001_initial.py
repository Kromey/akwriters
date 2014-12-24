# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginAudit',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('login_date', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('domain', models.CharField(max_length=30)),
                ('email', models.EmailField(null=True, max_length=75)),
                ('first_name', models.CharField(null=True, max_length=30)),
                ('last_name', models.CharField(null=True, max_length=30)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('timezone', models.CharField(null=True, max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to='prosodyauth.User')),
                ('email', models.EmailField(max_length=75)),
                ('token', models.CharField(max_length=40)),
                ('date_sent', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='loginaudit',
            name='user',
            field=models.ForeignKey(to='prosodyauth.User'),
            preserve_default=True,
        ),
    ]
