# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-27 14:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0012_auto_20180226_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracoes',
            name='data_validade_parecer',
            field=models.DateField(default=datetime.datetime(2018, 2, 27, 14, 17, 26, 969488)),
        ),
        migrations.AlterField(
            model_name='historicalconfiguracoes',
            name='data_validade_parecer',
            field=models.DateField(default=datetime.datetime(2018, 2, 27, 14, 17, 26, 969488)),
        ),
    ]