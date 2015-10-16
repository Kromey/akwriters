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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('host', models.TextField(default='fairbanksnano.org')),
                ('user', models.TextField()),
                ('store', models.TextField()),
                ('key', models.TextField()),
                ('type', models.TextField()),
                ('value', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
