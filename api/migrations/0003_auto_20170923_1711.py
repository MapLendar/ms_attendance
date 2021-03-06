# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-23 17:11
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170923_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='event_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(0), django.core.validators.MinValueValidator(2)]),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='user_id',
            field=models.BigIntegerField(),
        ),
    ]
