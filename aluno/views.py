# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from aluno.forms import CadastrarAlunoForm, PesquisarAlunoForm, EnderecoForm, MatriculaForm, DeclaracaoAlunoForm
from aluno.models import Aluno, Endereco, Matricula
from escola.models import Configuracoes
from util.utils import gerar_PDF

from datetime import datetime

@login_required
def cadastro_aluno(request):
	form = CadastrarAlunoForm()
	return render(request,'cadastro-aluno.html', {"form":form})

@login_required
def cadastrar_aluno(request):
	form     = CadastrarAlunoForm(request.POST)
	form_end = EnderecoForm(request.POST)
	if form.is_valid() and form_end.is_valid():
		endereco = form_end.save()
		aluno    = form.save(commit=False)
		aluno.endereco = endereco
		aluno.save()
		form.sucess = True
	
	return render(request,'cadastro-aluno.html', {"form":form, 'aluno':aluno})

@login_required
def edicao_aluno(request, aluno_id):
	form = CadastrarAlunoForm()
	aluno = Aluno.objects.get(id=aluno_id)
	return render(request, 'edicao-aluno.html', {"aluno":aluno, "form":form})

@login_required
def detalhe_aluno(request, aluno_id):
	aluno = Aluno.objects.get(id=aluno_id)
	return render(request, 'detalhe-aluno.html', {"aluno":aluno})

@login_required
def editar_aluno(request, aluno_id):
	aluno = Aluno.objects.get(id=aluno_id)
	form     = CadastrarAlunoForm(request.POST, instance=aluno)
	form_end = EnderecoForm(request.POST, instance=aluno.endereco)
	if form.is_valid() and form_end.is_valid():
		endereco = form_end.save()
		aluno    = form.save(commit=False)
		aluno.endereco = endereco
		aluno.save()
		form.sucess = True

	return render(request, 'edicao-aluno.html', {"aluno":aluno, "form":form,"form_end":form_end})

@login_required
def pesquisa_aluno(request):
	return render(request, 'pesquisa-aluno.html')

@login_required
def pesquisar_aluno(request):
	alunos = []
	form = PesquisarAlunoForm(request.POST)
	if form.is_valid():
		dados  = form.data
		alunos = Aluno.objects.filter(nome__icontains=dados['nome'])
		return render(request, 'pesquisa-aluno.html', {'form':form, "alunos":alunos})
	
	return render(request, 'pesquisa-aluno.html', {'form':form, "alunos":None})

@login_required
def matricula_aluno(request, aluno_id):
	form = MatriculaForm()
	aluno = Aluno.objects.get(id=aluno_id)
	ano_letivo =  Configuracoes.objects.get(id=1).ano_letivo
	matriculas =  aluno.matriculas.filter(ano=ano_letivo)
	matricula_atual = matriculas[0] if matriculas else None

	return render(request, 'matricula-aluno.html', {'form':form, 'aluno':aluno, 'ano_letivo': ano_letivo, 'matricula_atual':matricula_atual})

@login_required
def matricular_aluno(request, aluno_id):
	form = MatriculaForm(request.POST)
	aluno = Aluno.objects.get(id=aluno_id)
	ano_letivo =  Configuracoes.objects.get(id=1).ano_letivo
	matriculas = aluno.matriculas.filter(ano=ano_letivo)
	matricula_atual = matriculas[0] if matriculas else None

	if form.is_valid():
		dados = form.cleaned_data
		turma = dados['turma']
		ano   = dados['ano']
		transferido = dados['transferido']
		# verificar caso o aluno já tenha notas lancadas nessa serie ?
		if matricula_atual:
			matricula = matricula_atual
			matricula.turma = turma
			matricula.transferido = transferido
		else:
			matricula = Matricula(aluno=aluno, turma=turma, ano=ano)
		
		matricula.save()
		form.sucess = True

		return render(request, 'matricula-aluno.html', {'form':form, 'aluno':aluno, 'ano_letivo': ano, 'matricula_atual':matricula})

	return render(request, 'matricula-aluno.html', {'form':form, 'aluno':aluno, 'ano_letivo': ano_letivo, 'matricula_atual':matricula_atual})

@login_required
def declaracao_aluno(request, aluno_id):
	aluno = Aluno.objects.get(id=aluno_id)
	matriculas = aluno.matriculas.all()
	form = DeclaracaoAlunoForm()
	return render(request, 'declaracao-aluno.html', {'form':form, 'matriculas':matriculas, 'aluno':aluno})

@login_required
def emitir_declaracao_aluno(request, aluno_id):
	
	aluno = Aluno.objects.get(id=aluno_id)
	form = DeclaracaoAlunoForm(request.POST)
	matriculas = aluno.matriculas.all()
	if form.is_valid():
		dados = form.cleaned_data
		matricula = next(iter(aluno.matriculas.filter(ano=int(dados['ano']))), None)
		context = {'cidade':dados['cidade_declaracao'], 'texto':dados['texto'], 'aluno':aluno, 'matricula':matricula, 'data':datetime.now()}
		return gerar_PDF(request, context, 'template-declaracao-aluno', 'declaracao-'+aluno.nome)

	return render(request, 'declaracao-aluno.html', {'matriculas':matriculas, 'aluno':aluno, 'form':form})
