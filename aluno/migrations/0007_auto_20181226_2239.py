# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-26 22:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0006_auto_20181129_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmatricula',
            name='transferido',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='matricula',
            name='transferido',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalmatricula',
            name='data_matricula',
            field=models.DateField(default=datetime.date(2018, 12, 26)),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='data_matricula',
            field=models.DateField(default=datetime.date(2018, 12, 26)),
        ),
    ]
