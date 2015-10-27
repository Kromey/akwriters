# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import prosodyauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('prosodyauth', '0006_auto_20151016_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='date_sent',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='prosody',
            name='host',
            field=models.TextField(default=prosodyauth.models.getProsodyDomain),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='registrationconfirmation',
            name='date_sent',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
