# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-28 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rendimento', '0005_auto_20171228_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nota',
            name='tipo',
            field=models.IntegerField(choices=[(1, b'Nota Parcial'), (2, b'Nota Bimestral'), (2, b'Recupera\xc3\xa7\xc3\xa3o Paralela')]),
        ),
    ]