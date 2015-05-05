# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modcache',
            name='type',
            field=models.CharField(max_length=32, null=True),
            preserve_default=True,
        ),
    ]
