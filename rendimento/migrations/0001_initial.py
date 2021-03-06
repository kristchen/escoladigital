# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-28 15:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aluno', '0001_initial'),
        ('escola', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalNota',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=4)),
                ('bimestre', models.IntegerField(choices=[(1, b'1\xc2\xb0 Bimestre'), (2, b'2\xc2\xb0 Bimestre'), (3, b'3\xc2\xb0 Bimestre'), (4, b'4\xc2\xb0 Bimestre')])),
                ('tipo', models.IntegerField(choices=[(1, b'Nota Parcial'), (2, b'Nota Bimestral'), (4, b'Nota Extra'), (3, b'Recupera\xc3\xa7\xc3\xa3o')])),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('disciplina', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='escola.Disciplina')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('matricula', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='aluno.Matricula')),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical nota',
            },
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=4)),
                ('bimestre', models.IntegerField(choices=[(1, b'1\xc2\xb0 Bimestre'), (2, b'2\xc2\xb0 Bimestre'), (3, b'3\xc2\xb0 Bimestre'), (4, b'4\xc2\xb0 Bimestre')])),
                ('tipo', models.IntegerField(choices=[(1, b'Nota Parcial'), (2, b'Nota Bimestral'), (4, b'Nota Extra'), (3, b'Recupera\xc3\xa7\xc3\xa3o')])),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escola.Disciplina')),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notas', to='aluno.Matricula')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='nota',
            unique_together=set([('matricula', 'disciplina', 'bimestre', 'tipo')]),
        ),
    ]
