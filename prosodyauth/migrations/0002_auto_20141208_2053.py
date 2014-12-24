# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import prosodyauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('prosodyauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationConfirmation',
            fields=[
                ('user', models.OneToOneField(to='prosodyauth.User', serialize=False, primary_key=True)),
                ('token', models.CharField(default=prosodyauth.models.make_token, max_length=40)),
                ('date_sent', models.DateTimeField(auto_now=True)),
                ('password', models.CharField(max_length=40)),
                ('iterations', models.IntegerField(default=8192)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='emailconfirmation',
            name='token',
            field=models.CharField(default=prosodyauth.models.make_token, max_length=40),
            preserve_default=True,
        ),
    ]
