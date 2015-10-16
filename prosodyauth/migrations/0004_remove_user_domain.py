# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prosodyauth', '0003_prosody'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='domain',
        ),
    ]
