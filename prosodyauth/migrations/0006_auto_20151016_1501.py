# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prosodyauth', '0005_auto_20151016_1405'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='prosody',
            unique_together=set([('user', 'store', 'key')]),
        ),
    ]
