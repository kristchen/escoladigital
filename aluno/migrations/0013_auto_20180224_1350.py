# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-24 13:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0012_auto_20180218_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmatricula',
            name='data_matricula',
            field=models.DateField(default=datetime.date(2018, 2, 24)),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='data_matricula',
            field=models.DateField(default=datetime.date(2018, 2, 24)),
        ),
    ]