# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from simple_history.models import HistoricalRecords

from django.db import models
import choices
from aluno.models  import Matricula
from escola.models import Disciplina

class Nota(models.Model):

	matricula  = models.ForeignKey(Matricula, related_name='notas')
	disciplina = models.ForeignKey(Disciplina)
	valor = models.DecimalField(max_digits=4, decimal_places=2)
	bimestre = models.IntegerField(choices=choices.BIMESTRE_CHOICES)
	tipo  = models.IntegerField(choices=choices.TIPO_NOTA_CHOICES)
	history = HistoricalRecords()

	class Meta(object):
		unique_together = ('matricula','disciplina','bimestre','tipo')



		
