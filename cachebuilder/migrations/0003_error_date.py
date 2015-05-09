# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cachebuilder', '0002_auto_20150406_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='error',
            name='date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
