# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prosodyauth', '0004_remove_user_domain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosody',
            name='type',
            field=models.TextField(default='string'),
            preserve_default=True,
        ),
    ]
