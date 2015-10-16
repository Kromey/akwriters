# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prosodyauth', '0002_auto_20141208_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prosody',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('host', models.TextField(default='fairbanksnano.org')),
                ('user', models.TextField(db_index=True)),
                ('store', models.TextField(db_index=True)),
                ('key', models.TextField(db_index=True)),
                ('type', models.TextField()),
                ('value', models.TextField()),
            ],
            options={
                'db_table': 'prosody',
            },
            bases=(models.Model,),
        ),
    ]
