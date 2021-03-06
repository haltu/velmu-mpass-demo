# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-29 09:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('mpass', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('service_id', models.CharField(max_length=128)),
                ('icon_url', models.CharField(blank=True, max_length=2048, null=True)),
                ('service_url', models.CharField(blank=True, max_length=2048, null=True)),
                ('sso_url', models.CharField(blank=True, max_length=2048, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ServiceTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('description', models.CharField(max_length=2048)),
                ('title', models.CharField(max_length=2048)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='mpass.Service')),
            ],
            options={
                'managed': True,
                'db_table': 'mpass_service_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'service Translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='servicetranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
