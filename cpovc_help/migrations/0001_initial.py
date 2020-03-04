# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OVCDownloads',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doc_type', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('version', models.DecimalField(max_digits=5, decimal_places=2)),
                ('doc_date', models.DateField()),
                ('doc_details', models.TextField()),
                ('downloads', models.BigIntegerField(default=0)),
                ('doc_tags', models.CharField(max_length=255)),
                ('document', models.FileField(upload_to=b'documents')),
                ('is_public', models.BooleanField(default=False)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_downloads',
                'verbose_name': 'DCS / OVC Document',
                'verbose_name_plural': 'DCS / OVC Documents',
            },
        ),
        migrations.CreateModel(
            name='OVCFAQ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('faq_order', models.IntegerField(default=1)),
                ('faq_title', models.CharField(max_length=255)),
                ('faq_details', models.TextField()),
                ('faq_timestamp', models.DateTimeField()),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_faq',
                'verbose_name': 'FAQ Detail',
                'verbose_name_plural': 'FAQ Details',
            },
        ),
    ]
