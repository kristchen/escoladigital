# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from forms import SerieForm, DisciplinaForm, TurmaForm, ConfiguracoesForm
from models import Serie, Disciplina, Turma, Curriculo, Configuracoes
from aluno.models import Matricula

@login_required
def cadastro_serie(request):
	form = SerieForm()
	return render(request,'associar-disciplina-serie.html', {"form":form})

@login_required
def cadastro_disciplina(request):
	disciplinas = Disciplina.objects.all()
	form = DisciplinaForm()
	return render(request,'cadastro-disciplina.html', {"form":form, "disciplinas":disciplinas})

@login_required
def alterar_status_disciplina(request, disciplina_id):
	disciplina = Disciplina.objects.get(id=disciplina_id)
	disciplina.ativa = False if disciplina.ativa else True 	
	
	disciplina.save()
	data = serializers.serialize("json", [disciplina])
	
	return HttpResponse(data, content_type='application/json') 

@login_required
def edicao_disciplina(request, disciplina_id):
	disciplina = Disciplina.objects.get(pk=disciplina_id)
	form = DisciplinaForm()
	return render(request,'edicao-disciplina.html', {"form":form, "disciplina":disciplina})

@login_required
def editar_disciplina(request, disciplina_id):
	disciplina = Disciplina.objects.get(pk=disciplina_id)
	form = DisciplinaForm(request.POST, instance=disciplina)
	if form.is_valid():
		form.save()
		form.sucess = True
	return render(request,'edicao-disciplina.html', {"form":form, "disciplina":disciplina})

@login_required
def cadastrar_disciplina(request):
	form = DisciplinaForm(request.POST)
	if form.is_valid():
		form.save()
		form.sucess = True
	disciplinas = Disciplina.objects.all()
	return render(request,'cadastro-disciplina.html', {"form":form, "disciplinas":disciplinas})

@login_required
def cadastro_turma(request):
	turmas = Turma.objects.all()
	form = TurmaForm()
	return render(request,'cadastro-turma.html', {"form":form, "turmas":turmas})

@login_required
def cadastrar_turma(request):
	form = TurmaForm(request.POST)
	if form.is_valid():
		form.save()
		form.sucess = True
	turmas = Turma.objects.all()
	return render(request,'cadastro-turma.html', {"form":form, "turmas":turmas})

@login_required
def alterar_status_turma(request, turma_id):
	turma = Turma.objects.get(id=turma_id)
	turma.ativa = False if turma.ativa else True 	
	
	turma.save()
	data = serializers.serialize("json", [turma])
	
	return HttpResponse(data, content_type='application/json') 

@login_required
def lista_disciplinas_serie(request, serie_id):
	disciplinas_salvas_ativa = [ x.disciplina.id for x in Curriculo.objects.filter(serie_id=serie_id) if x.ativo] 
	form = SerieForm()
	return render(request,'disciplinas-serie.html', {"form":form, "disciplinas_salvas":disciplinas_salvas_ativa})	

@login_required
def lista_disciplinas_serie_historico(request, serie_id):
	serie = Serie.objects.get(id=serie_id)
	form = SerieForm()
	return render(request,'disciplinas-serie-historico.html', {"form":form, 'curriculos':serie.curriculos.all()})	

@login_required
def lista_disciplinas_serie_rendimento(request, serie_id):
	serie = Serie.objects.get(id=serie_id)
	disciplinas_salvas_ativa = [ x.disciplina for x in Curriculo.objects.filter(serie_id=serie_id) if x.ativo and not x.disciplina.somente_historico] 
	return render(request,'disciplinas-serie-rendimento.html', {'disciplinas':disciplinas_salvas_ativa})	

@login_required
def associar_disciplina(request):
	form = SerieForm(request.POST)
	if form.is_valid():
		dados = form.cleaned_data
		serie =  dados['series']
		disciplinas =  [ d.id for d in dados['disciplinas']]
		curriculos = serie.curriculos.all() 

		# Ativar os que existirem e vieram do form e desativar as que existem e não vieram do form
		for c in curriculos:
			if c.disciplina.id in disciplinas and not c.ativo:
				c.ativo = True
				c.save()
			elif c.disciplina.id not in disciplinas and c.ativo:
				c.ativo = False
				c.save()	
		# as que vieram do form e não existem, cria-se
		for d in disciplinas:
			if d not in [cr.disciplina.id for cr in curriculos]:
				curriculo = Curriculo(serie=serie, disciplina=Disciplina(id=d))
				curriculo.save()

		form.sucess = True

	return render(request,'associar-disciplina-serie.html', {"form":form})

@login_required
def edicao_configuracoes(request):
	form = ConfiguracoesForm()
	confs = Configuracoes.objects.get(id=1)
	return render(request,'edicao-configuracoes.html', {"form":form, "confs":confs})

@login_required
def editar_configuracoes(request):
	confs = Configuracoes.objects.get(id=1)
	form  = ConfiguracoesForm(request.POST, instance=confs)
	if form.is_valid():
		form.save()
		form.sucess = True
	
	return render(request,'edicao-configuracoes.html', {"form":form, "confs":confs})