# Generated by Django 2.2.6 on 2019-11-12 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_characternotesanswer_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='age',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
