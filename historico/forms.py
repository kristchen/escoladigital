# -*- coding: utf-8 -*-
from django import forms
import choices
from models import Historico
from escola.models import Serie


class HistoricoForm(forms.Form):
	ano = forms.ChoiceField(choices=choices.ANO_HISTORICO_CHOICES, required=True, error_messages={'required': 'Informe o ano corretamente.'})
	serie = forms.ModelChoiceField(queryset=Serie.objects.all(), required=True, error_messages={'required':'A série deve ser informada.'})
	situacao = forms.ChoiceField(choices=choices.SITUACAO_CHOICES, required=True, error_messages={'required': 'Informe a situação corretamente.'})
	uf = forms.ChoiceField(choices=choices.UF_CHOICES, required=True, error_messages={'required': 'Informe a situação corretamente.'})
