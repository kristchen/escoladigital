# -*- coding: utf-8 -*-
from django import forms
import choices

from models import Nota
from escola.models import Disciplina

class NotaForm(forms.ModelForm):
	bimestre = forms.ChoiceField(choices=choices.BIMESTRE_CHOICES, required=True, error_messages={'required':'Informe o bimestre de referência.'})
	tipo = forms.ChoiceField(choices=choices.TIPO_NOTA_CHOICES, required=True, error_messages={'required':'Informe o tipo de nota.'})
	disciplinas = forms.ModelChoiceField(queryset=Disciplina.objects.all(), required=True, error_messages={'required':'Informe a disciplina'})
	valor = forms.DecimalField(required=True)
	conceitos = forms.ChoiceField(choices=choices.NOTA_CONCEITO_CHOICES, required=False)

	class Meta(object):
		model  = Nota
		fields = ('tipo', 'bimestre', 'valor','matricula')