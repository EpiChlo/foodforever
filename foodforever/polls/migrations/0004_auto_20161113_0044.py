# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 05:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20161112_2145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='question',
            new_name='ingredient',
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='exp_date',
            field=models.DateField(verbose_name='expiration date'),
        ),
    ]
