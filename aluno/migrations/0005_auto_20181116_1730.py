# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-16 17:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0004_auto_20180428_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmatricula',
            name='data_matricula',
            field=models.DateField(default=datetime.date(2018, 11, 16)),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='data_matricula',
            field=models.DateField(default=datetime.date(2018, 11, 16)),
        ),
    ]
