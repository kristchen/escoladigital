# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from simple_history.models import HistoricalRecords
import choices
from datetime import datetime

class Disciplina(models.Model):
	descricao = models.CharField(null=False, max_length=255)
	base_nacional_comum = models.BooleanField(default=True)
	somente_historico = models.BooleanField(default=False)
	ativa = models.BooleanField(default=True)
	history = HistoricalRecords()

class Serie(models.Model):
	descricao   = models.CharField(max_length=255, null=False, choices=choices.SERIES_CHOICES)
	modalidade  = models.CharField(null=False, choices=choices.MODALIDADE_ENSINO_CHOICES, max_length=1)
	ativa = models.BooleanField(default=True)
	history = HistoricalRecords()

	class Meta(object):
		unique_together = ('descricao', 'modalidade')

class Curriculo(models.Model):
	disciplina = models.ForeignKey(Disciplina)
	serie = models.ForeignKey(Serie, related_name='curriculos')
	ativo = models.BooleanField(default=True)
	history = HistoricalRecords()
	
	class Meta(object):
		unique_together = ('disciplina', 'serie', 'ativo')

class Turma(models.Model):
	serie = models.ForeignKey(Serie, related_name='turmas')
	sequencia = models.CharField(null=False, max_length=1, choices=choices.TURMA_SEQUENCIA_CHOICES)			
	ativa = models.BooleanField(default=True)
	history = HistoricalRecords()
	
	class Meta(object):
		unique_together = ('serie', 'sequencia')

class Configuracoes(models.Model):
	media = models.DecimalField(max_digits=4, decimal_places=2, null=False)
	ano_letivo = models.PositiveIntegerField(null=False)
	parecer = models.CharField(null=False, max_length=255, default='111111/1111')
	data_validade_parecer = models.DateField(default=datetime.now())
	history = HistoricalRecords()
		

		


