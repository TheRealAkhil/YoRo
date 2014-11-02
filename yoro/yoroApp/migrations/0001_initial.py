# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=30)),
                ('text_body', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(verbose_name=b'Start Date')),
                ('exp_date', models.DateTimeField(verbose_name=b'Expiration Date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
