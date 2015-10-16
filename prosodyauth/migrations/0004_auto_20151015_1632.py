# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prosodyauth', '0003_prosody'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosody',
            name='key',
            field=models.TextField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='prosody',
            name='store',
            field=models.TextField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='prosody',
            name='user',
            field=models.TextField(db_index=True),
            preserve_default=True,
        ),
    ]
