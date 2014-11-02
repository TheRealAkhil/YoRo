# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=30)),
                ('text_body', models.CharField(max_length=200)),
                ('time', models.DateTimeField(verbose_name=b'Reminder Date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
