# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from itertools import chain, groupby

from aluno.models import Aluno
from escola.models import Serie, Disciplina, Configuracoes
from escola import choices
from models import Historico, Nota, Instituicao
from historico.forms import HistoricoForm
from rendimento.choices import RECUPERACAO, RECUPERACAO_FINAL
import json
import numpy as np
from django.db import transaction
from util.utils import gerar_PDF, normal_round



@login_required
def cadastro_historico(request, aluno_id):
	aluno = Aluno.objects.get(id=aluno_id)
	form = HistoricoForm()
	return render(request, 'cadastro-historico.html', {'aluno':aluno, 'form':form})


@login_required
@transaction.atomic
def cadastrar_historico(request, aluno_id):
	data = json.loads(json.loads(json.dumps(request.POST)).get('historico'))
	aluno = Aluno.objects.get(id=aluno_id)
	serie = Serie.objects.get(id=data['serie'])

	jsonInstituicao = data.get('instituicao')

	if jsonInstituicao.get('id'):
		instituicao =  Instituicao.objects.get(id=jsonInstituicao['id'])
	else:
		instituicao = Instituicao(descricao=jsonInstituicao['descricao'], uf=jsonInstituicao['uf'], cidade=jsonInstituicao['cidade'])
		instituicao.save()

	historico = Historico(instituicao=instituicao, situacao=data['situacao'], carga_horaria=data['carga'], serie=serie, ano=data['ano'], aluno=aluno)
	historico.save()
	for notaJSON in data.get('notas'):
		disciplina = Disciplina.objects.get(id=notaJSON['disciplina'])
		nota = Nota(disciplina=disciplina, valor=notaJSON['valor'], historico=historico)
		nota.save()

	return HttpResponse('{"sucess":true}', content_type='application/json')


@login_required
def detalhe_historico(request, aluno_id):
	aluno = Aluno.objects.get(id=aluno_id)
	return render(request, 'detalhe-historico.html', {'aluno':aluno, 'historicos':aluno.historicos.all()})


@login_required
def edicao_historico(request, historico_id):
	form = HistoricoForm()
	historico = Historico.objects.get(id=historico_id)
	return render(request, 'edicao-historico.html', {'form':form, 'aluno':historico.aluno, 'notas':historico.notas.all(), 'historico':historico})


@login_required
def excluir_historico(request, historico_id):
	form = HistoricoForm()
	historico = Historico.objects.get(id=historico_id)
	aluno = historico.aluno
	historico.delete()
	form.delete = True

	return render(request, 'detalhe-historico.html', {'form':form, 'aluno':aluno, 'historicos':aluno.historicos.all()})


@login_required
def lista_instituicoes_historico(request):
	data = json.loads(json.dumps(request.POST)).get('value')
	instituicoes = Instituicao.objects.filter(descricao__icontains=data)
	lista = serializers.serialize('json', instituicoes)
	return HttpResponse(lista, content_type='application/json')


@login_required
@transaction.atomic
def editar_historico(request):
	data = json.loads(json.loads(json.dumps(request.POST)).get('historico'))
	serie = Serie.objects.get(id=data['serie'])

	jsonInstituicao = data.get('instituicao')
	if jsonInstituicao.get('id'):
		instituicao = Instituicao.objects.get(id=jsonInstituicao['id'])
		instituicao.descricao = jsonInstituicao['descricao'] 
		instituicao.uf = jsonInstituicao['uf'] 
		instituicao.cidade = jsonInstituicao['cidade']
		instituicao.save()
	else:
		instituicao = Instituicao(descricao=jsonInstituicao['descricao'], uf=jsonInstituicao['uf'], cidade=jsonInstituicao['cidade'])
		instituicao.save()

	historico = Historico.objects.get(id=data['id_historico'])
	historico.situacao = data['situacao'] 
	historico.carga_horaria = data['carga']
	historico.serie = serie
	historico.instituicao = instituicao 
	historico.ano = data['ano']
	historico.save()

	for notaJSON in data.get('notas'):
		nota = Nota.objects.get(id=notaJSON['id'])
		nota.valor = notaJSON['valor']
		nota.save()

	return HttpResponse('{"sucess":true}', content_type='application/json')

@login_required
def emitir_historico(request, aluno_id):
	confs = Configuracoes.objects.get(id=1)
	aluno = Aluno.objects.get(id=aluno_id)
	disciplinas   = Disciplina.objects.all()
	series = Serie.objects.filter(modalidade=choices.MODALIDADE_FUNDAMENTAL)
	notas_historico = list(chain.from_iterable([historico.notas.all() for historico in aluno.historicos.all()]))

	for dis in disciplinas:
		dis.notas = np.full(9, None)
		notas_disciplina = [nota for nota in notas_historico if nota.disciplina.id == dis.id]
		for idx, serie in enumerate(series):
			nota = [nota for nota in notas_disciplina if nota.historico.serie.id == serie.id]
			if nota:
				dis.notas[idx] = nota[0]

	diversificada = filter(lambda x : not x.base_nacional_comum, disciplinas)
	base_nacional = filter(lambda x : x.base_nacional_comum, disciplinas)

	context = {'aluno':aluno,
	'confs':confs,
	'carga_horaria':get_carga_horaria(aluno, series),
	'historicos':aluno.historicos.all(),
	'rowspan_diversificada':len(diversificada) + 1, 
	'diversificada':diversificada, 
	'rowspan_base':len(base_nacional) +1, 
	'base_nacional':base_nacional}

	return gerar_PDF(request, context, 'template-historico-escolar-aluno', 'historico-'+aluno.nome)

	# return render(request, 'template-historico-escolar-aluno.html', context)

@login_required
def consolidar_historico(request, aluno_id):
	aluno = Aluno.objects.get(id=aluno_id)
	confs = Configuracoes.objects.get(id=1)
	matriculas = aluno.matriculas.exclude(ano=confs.ano_letivo)
	cbms = Instituicao.objects.get(id=1)
	for matricula in matriculas:
		historico = Historico.objects.filter(ano=matricula.ano, aluno=aluno)
		grupo_notas_disciplina = groupby(matricula.notas.all(), lambda x: x.disciplina)
		if historico:
			for key, value in grupo_notas_disciplina:
				notas = [nt for nt in value]
				nota = historico.notas.filter(disciplina=key)
				nota.valor = get_nota_historico(notas)
				nota.save()

		else:
			historico = Historico(instituicao=cbms, situacao=True, carga_horaria=200, serie=matricula.turma.serie, ano=matricula.ano, aluno=aluno)
			historico.save()
			for key, value in grupo_notas_disciplina:
				notas = [nt for nt in value]
				valor = get_nota_historico(notas)
				if valor < confs.media and historico.situacao:
					historico.situacao=False
					historico.save()
				nota = Nota(disciplina=key, valor=valor, historico=historico)
				nota.save()
	
	return HttpResponse('{"sucess":true}', content_type='application/json')


def get_nota_historico(notas):
	
	rec_final = next(( n for n in notas if n.bimestre == long(RECUPERACAO_FINAL) and n.tipo == choices.RECUPERACAO), None)
	
	medias_bimestrais = []
	
	for x, y in choices.BIMESTRE_CHOICES:	
		notas_bimestre = [n.valor for n in notas if n.bimestre == x and n.tipo != RECUPERACAO]
		nota_recuperacao = [n.valor for n in notas if n.bimestre == x and n.tipo == RECUPERACAO]
		media_bimestral = sum(notas_bimestre)/3
		medias_bimestrais.append(nota_recuperacao[0] if nota_recuperacao and nota_recuperacao[0] > media_bimestral else media_bimestral)

	return rec_final if rec_final else normal_round(sum(medias_bimestrais)/4)


def get_carga_horaria(aluno, series):
	carga_horaria = np.full(9, None)

	for idx, serie in enumerate(series):
		carga_horaria[idx] = next(iter([historico.carga_horaria for historico in aluno.historicos.all() if historico.serie.id == serie.id]), None)

	return  carga_horaria