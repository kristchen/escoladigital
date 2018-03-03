# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-18 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0009_remove_serie_disciplinas'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplina',
            name='somente_historico',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicaldisciplina',
            name='somente_historico',
            field=models.BooleanField(default=False),
        ),
    ]
