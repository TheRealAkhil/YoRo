# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yoroApp', '0002_note_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='flagRead',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
