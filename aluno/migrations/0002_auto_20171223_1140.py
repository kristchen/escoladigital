# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-23 11:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matricula',
            name='data_matricula',
            field=models.DateField(default=datetime.date(2017, 12, 23)),
        ),
    ]