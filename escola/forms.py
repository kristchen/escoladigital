# -*- coding: utf-8 -*-
from django import forms
import choices
from models import Disciplina, Serie, Turma, Configuracoes

class SerieForm(forms.ModelForm):
	series = forms.ModelChoiceField(queryset=Serie.objects.all(), required=True, error_messages={'required': 'Informe a série.'})
	disciplinas = forms.ModelMultipleChoiceField(queryset=Disciplina.objects.all(), required=True, error_messages={'required': 'A série deve conter ao menos uma disciplina.'})

	class Meta:
	    model  = Serie
	    fields = ('series', 'disciplinas')
			
class DisciplinaForm(forms.ModelForm):
	descricao = forms.CharField(required=True, error_messages={'required': 'Informe a descricao.'})
	base_nacional_comum = forms.BooleanField(required=False)
	somente_historico = forms.BooleanField(required=False)

	class Meta:
		model  = Disciplina
		fields = ('descricao','base_nacional_comum','somente_historico')

class TurmaForm(forms.ModelForm):
	serie = forms.ModelChoiceField(queryset=Serie.objects.all(), required=True, error_messages={'required':'A série deve ser informada'})
	sequencia = forms.ChoiceField(choices=choices.TURMA_SEQUENCIA_CHOICES, required=True)

	class Meta:
		model  = Turma
		fields = ('serie','sequencia')

class ConfiguracoesForm(forms.ModelForm):
	media = forms.IntegerField(required=True, error_messages={'required': 'Informe a média'})
	ano_letivo = forms.ChoiceField(choices=choices.ANO_LETIVO_CHOICES, required=True, error_messages={'required': 'Informe o ano letivo.'})
	data_validade_parecer = forms.DateField(required=True, error_messages={'required': 'Informe a data de validade do parecer'})
	parecer = forms.CharField(required=True, error_messages={'required': 'Informe o número do parecer.'})

	class Meta:
		model  = Configuracoes
		fields = ('media', 'ano_letivo', 'data_validade_parecer', 'parecer')