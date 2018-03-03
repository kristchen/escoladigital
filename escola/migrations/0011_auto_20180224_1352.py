# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-24 13:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0010_auto_20180218_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracoes',
            name='parecer',
            field=models.CharField(default='111111/1111', max_length=255),
        ),
        migrations.AddField(
            model_name='configuracoes',
            name='validade_parecer',
            field=models.DateField(default=datetime.datetime(2018, 2, 24, 13, 52, 8, 253861)),
        ),
        migrations.AddField(
            model_name='historicalconfiguracoes',
            name='parecer',
            field=models.CharField(default='111111/1111', max_length=255),
        ),
        migrations.AddField(
            model_name='historicalconfiguracoes',
            name='validade_parecer',
            field=models.DateField(default=datetime.datetime(2018, 2, 24, 13, 52, 8, 253861)),
        ),
        migrations.AlterField(
            model_name='historicalserie',
            name='descricao',
            field=models.CharField(choices=[('Infantil I', 'Infantil I'), ('Infantil II', 'Infantil II'), ('Infantil III', 'Infantil III'), ('Infantil IV', 'Infantil IV'), ('Infantil V', 'Infantil V'), ('1\xb0 Ano', '1\xb0 Ano'), ('2\xb0 Ano', '2\xb0 Ano'), ('3\xb0 Ano', '3\xb0 Ano'), ('4\xb0 Ano', '4\xb0 Ano'), ('5\xb0 Ano', '5\xb0 Ano'), ('6\xb0 Ano', '6\xb0 Ano'), ('7\xb0 Ano', '7\xb0 Ano'), ('8\xb0 Ano', '8\xb0 Ano'), ('9\xb0 Ano', '9\xb0 Ano')], max_length=255),
        ),
        migrations.AlterField(
            model_name='serie',
            name='descricao',
            field=models.CharField(choices=[('Infantil I', 'Infantil I'), ('Infantil II', 'Infantil II'), ('Infantil III', 'Infantil III'), ('Infantil IV', 'Infantil IV'), ('Infantil V', 'Infantil V'), ('1\xb0 Ano', '1\xb0 Ano'), ('2\xb0 Ano', '2\xb0 Ano'), ('3\xb0 Ano', '3\xb0 Ano'), ('4\xb0 Ano', '4\xb0 Ano'), ('5\xb0 Ano', '5\xb0 Ano'), ('6\xb0 Ano', '6\xb0 Ano'), ('7\xb0 Ano', '7\xb0 Ano'), ('8\xb0 Ano', '8\xb0 Ano'), ('9\xb0 Ano', '9\xb0 Ano')], max_length=255),
        ),
    ]
