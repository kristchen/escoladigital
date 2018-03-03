# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from escola.models import Serie, Disciplina
from aluno.models import Aluno
from simple_history.models import HistoricalRecords


class Instituicao(models.Model):

	descricao = models.CharField(max_length=255, null=False)
	cidade = models.CharField(max_length=255, null=False)
	uf = models.CharField(max_length=2, null=False)
	history = HistoricalRecords()

	class Meta(object):
		unique_together = ('descricao',)	

class Historico(models.Model):

	instituicao = models.ForeignKey(Instituicao)
	ano = models.PositiveIntegerField(null=False)
	carga_horaria = models.PositiveIntegerField(null=False)
	serie = models.ForeignKey(Serie)
	aluno = models.ForeignKey(Aluno, related_name='historicos')
	situacao = models.BooleanField(default=True)
	history = HistoricalRecords()

	class Meta(object):
		unique_together = ('ano','aluno')	

class Nota(models.Model):

	valor = models.DecimalField(max_digits=4, decimal_places=2)
	disciplina = models.ForeignKey(Disciplina, related_name='disciplina_historico')
	historico = models.ForeignKey(Historico, related_name='notas')
	history = HistoricalRecords()


