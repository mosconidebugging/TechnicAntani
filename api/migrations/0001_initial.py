# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=64)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModCache',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('localpath', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=32)),
                ('md5', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModInfoCache',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('pretty_name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('link', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModpackCache',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('logo_md5', models.CharField(max_length=32)),
                ('icon_md5', models.CharField(max_length=32)),
                ('background_md5', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionCache',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=32)),
                ('recommended', models.BooleanField(default=False)),
                ('latest', models.BooleanField(default=False)),
                ('mcversion', models.CharField(max_length=32)),
                ('mcversion_checksum', models.CharField(max_length=32)),
                ('forgever', models.CharField(max_length=64)),
                ('modpack', models.ForeignKey(to='api.ModpackCache')),
                ('mods', models.ManyToManyField(to='api.ModCache')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='modcache',
            name='modInfo',
            field=models.ForeignKey(to='api.ModInfoCache'),
            preserve_default=True,
        ),
    ]
