# -*- coding: utf-8 -*-

from django import forms
from escola import choices
from escola.models import Serie, Disciplina

class TurmaRelatorioForm(forms.Form):
	serie = forms.ModelChoiceField(queryset=Serie.objects.all(), required=True, error_messages={'required':'A série deve ser informada'})
	sequencia = forms.ChoiceField(choices=choices.TURMA_SEQUENCIA_CHOICES, required=False)

class SituacaoFinalDisciplinaRelatorioForm(forms.Form):
	disciplina = forms.ModelChoiceField(queryset=Disciplina.objects.all(), required=True,  error_messages={'required':'A disciplina deve ser informada'})
	situacao = forms.CharField(max_length=1, required=False)