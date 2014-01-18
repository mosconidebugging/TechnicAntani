# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ApiKey'
        db.create_table('api_apikey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('api', ['ApiKey'])

        # Adding model 'ModpackCache'
        db.create_table('api_modpackcache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('logo_md5', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('icon_md5', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('background_md5', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('api', ['ModpackCache'])

        # Adding model 'ModInfoCache'
        db.create_table('api_modinfocache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('pretty_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('api', ['ModInfoCache'])

        # Adding model 'ModCache'
        db.create_table('api_modcache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('localpath', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('modInfo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.ModInfoCache'])),
        ))
        db.send_create_signal('api', ['ModCache'])

        # Adding model 'VersionsCache'
        db.create_table('api_versionscache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('recommended', self.gf('django.db.models.fields.BooleanField')()),
            ('latest', self.gf('django.db.models.fields.BooleanField')()),
            ('mcversion', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('mcversion_checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('forgever', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('modpack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.ModpackCache'])),
        ))
        db.send_create_signal('api', ['VersionsCache'])

        # Adding M2M table for field mods on 'VersionsCache'
        m2m_table_name = db.shorten_name('api_versionscache_mods')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('versionscache', models.ForeignKey(orm['api.versionscache'], null=False)),
            ('modcache', models.ForeignKey(orm['api.modcache'], null=False))
        ))
        db.create_unique(m2m_table_name, ['versionscache_id', 'modcache_id'])


    def backwards(self, orm):
        # Deleting model 'ApiKey'
        db.delete_table('api_apikey')

        # Deleting model 'ModpackCache'
        db.delete_table('api_modpackcache')

        # Deleting model 'ModInfoCache'
        db.delete_table('api_modinfocache')

        # Deleting model 'ModCache'
        db.delete_table('api_modcache')

        # Deleting model 'VersionsCache'
        db.delete_table('api_versionscache')

        # Removing M2M table for field mods on 'VersionsCache'
        db.delete_table(db.shorten_name('api_versionscache_mods'))


    models = {
        'api.apikey': {
            'Meta': {'object_name': 'ApiKey'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'api.modcache': {
            'Meta': {'object_name': 'ModCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localpath': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'modInfo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.ModInfoCache']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'api.modinfocache': {
            'Meta': {'object_name': 'ModInfoCache'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pretty_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'api.modpackcache': {
            'Meta': {'object_name': 'ModpackCache'},
            'background_md5': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'icon_md5': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_md5': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'api.versionscache': {
            'Meta': {'object_name': 'VersionsCache'},
            'forgever': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.BooleanField', [], {}),
            'mcversion': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'mcversion_checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'modpack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.ModpackCache']"}),
            'mods': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['api.ModCache']"}),
            'recommended': ('django.db.models.fields.BooleanField', [], {}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['api']