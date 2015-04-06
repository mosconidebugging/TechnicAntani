# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cachebuilder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='error',
            name='style',
            field=models.CharField(max_length=63, default='info'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='error',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
