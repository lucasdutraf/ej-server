# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-07 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('math', '0003_auto_20180117_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('STARTED', 'STARTED'), ('FINISHED', 'FINISHED'), ('FAILED', 'FAILED'), ('STUCKED', 'STUCKED')], default='PENDING', max_length=20, verbose_name='Status'),
        ),
    ]