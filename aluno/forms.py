# -*- coding: utf-8 -*-
from django import forms
import choices

from models import Aluno, Endereco, Matricula
from escola.models import Turma

class CadastrarAlunoForm(forms.ModelForm):

	nome = forms.CharField(required=True, error_messages={'required': 'Informe o nome do aluno corretamente.'})
	data_nascimento = forms.DateField(required=True, error_messages={'required': 'Informe o data de nascimento do aluno corretamente.'})
	sexo = forms.ChoiceField(choices=choices.SEXO_CHOICES, required=True, error_messages={'required': 'Informe o sexo do aluno corretamente.'})
	telefone = forms.IntegerField(required=True, error_messages={'required': 'Informe o telefone para contato.'})
	nome_mae = forms.CharField(required=True, error_messages={'required': 'Informe o nome da mãe do aluno corretamente.'})
	nome_pai = forms.CharField(required=True, error_messages={'required': 'Informe o nome do pai do aluno corretamente.'})
	nome_responsavel = forms.CharField(required=False)


	class Meta(object):
		model = Aluno
		fields = ('nome', 'data_nascimento', 'sexo', 'telefone', 'nome_pai', 'nome_mae','nome_responsavel')


class EnderecoForm(forms.ModelForm):
	
	cep = forms.IntegerField(required=False)
	logradouro = forms.CharField(required=True, error_messages={'required': 'Informe o logradouro corretamente.'})
	numero = forms.IntegerField(required=True, error_messages={'required': 'Informe o número da residência corretamente.'})
	complemento = forms.CharField(required=False)
	
	bairro = forms.CharField(required=True, error_messages={'required': 'Informe o nome do bairro corretamente.'})
	cidade = forms.CharField(required=True, error_messages={'required': 'Informe o nome da cidade corretamente.'})
	
	class Meta(object):
		model  = Endereco
		fields = ('cep','logradouro','numero','complemento','bairro','cidade')	

class PesquisarAlunoForm(forms.ModelForm):
	nome = forms.CharField(required=True, error_messages={'required': 'Informe o nome do aluno para pequisar.'})

	class Meta(object):
		model = Aluno
		fields = ('nome',)		

class DeclaracaoAlunoForm(forms.Form):
	ano = forms.IntegerField(required=True, error_messages={'required':'Informe o letivo.'})
	texto = forms.CharField(required=False)
	tipo = forms.ChoiceField(choices=choices.TIPO_DECLARACAO_CHOICES, required=True, error_messages={'required': 'Informe o tipo da declaração'})
	cidade_declaracao =forms.ChoiceField(choices=choices.CIDADE_DECLARACAO_CHOICES, required=True, error_messages={'required': 'Informe a cidade corretamente.'})

class MatriculaForm(forms.ModelForm):
	
	turma = forms.ModelChoiceField(queryset=Turma.objects.filter(ativa=True), required=True,   error_messages={'required':'Informe a turma.'})
	ano   = forms.IntegerField(required=True, error_messages={'required':'Informe o ano de matrícula.'})
	transferido = forms.BooleanField(required=False)

	class Meta(object):
		model = Matricula
		fields = ('turma','ano', 'transferido')	






