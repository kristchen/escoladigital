# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
import datetime
from util.utils import gerar_numero_matricula
from simple_history.models import HistoricalRecords

from escola.models import Turma

class Endereco(models.Model):

	cep = models.PositiveIntegerField(null=True)
	logradouro = models.CharField(null=False, max_length=255)
	numero = models.PositiveIntegerField()
	bairro = models.CharField(max_length=255, null=False)
	cidade = models.CharField(max_length=255, null=False)
	complemento = models.CharField(max_length=255)
	history = HistoricalRecords()


class Aluno(models.Model):
	
	nome = models.CharField(max_length=255, null=False)
	data_nascimento = models.DateField()
	nome_pai = models.CharField(max_length=255, null=False)
	nome_mae = models.CharField(max_length=255, null=False)
	nome_responsavel = models.CharField(max_length=255, null=False)
	endereco = models.ForeignKey(Endereco)
	telefone = models.PositiveIntegerField(null=False)
	sexo = models.CharField(null=False, max_length=1)
	history = HistoricalRecords()

	def save(self, *args, **kwargs):
		self.nome = self.nome.upper()
		super(Aluno, self).save(*args, **kwargs)


class Matricula(models.Model):
	
	aluno = models.ForeignKey(Aluno, related_name='matriculas')
	turma = models.ForeignKey(Turma, related_name='alunos')
	data_matricula = models.DateField(auto_now=False, default=datetime.date.today())
	ano = models.PositiveIntegerField(null=False)
	numero = models.CharField(unique=True, max_length=255, default='0')
	transferido = models.BooleanField(default=False)
	history = HistoricalRecords()
		
	class Meta(object):
		unique_together = ('aluno','turma','ano')

	def save(self, *args, **kwargs):
		if self.numero == '0':
			self.numero = gerar_numero_matricula()
		super(Matricula, self).save(*args, **kwargs)








		

