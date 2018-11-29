# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse

import choices
from escola.models import Turma, Configuracoes, Curriculo, Disciplina
from escola.choices import MODALIDADE_INFANTIL
from aluno.models import Matricula

from forms import NotaForm
from models import Nota
from util.utils import gerar_PDF, normal_round

from itertools import groupby
from collections import Counter
import numpy as np
import json
from datetime import datetime

@login_required
def cadastro_notas(request):
	confs = Configuracoes.objects.get(id=1)
	form = NotaForm()
	return render(request, 'cadastro-notas.html', {'ano':confs.ano_letivo,'form':form, 'turmas':Turma.objects.all()})

@login_required
def cadastro_notas_recuperacao_final(request):
	confs = Configuracoes.objects.get(id=1)
	form = NotaForm()
	context = {'ano':confs.ano_letivo,'choices':choices, 'turmas':Turma.objects.all(), 'form':form}
	return render(request, 'cadastro-notas-recuperacao-final.html', context)

@login_required
def cadastrar_notas(request):

	data = json.loads(json.dumps(request.POST))
	for notaJSON in json.loads(data.get('notas')):
		matricula = Matricula.objects.get(id=notaJSON['matricula'])
		nota = matricula.notas.filter(disciplina_id=notaJSON['disciplina'], bimestre=notaJSON['bimestre'], tipo=notaJSON['tipo'])
   		if nota:
   			nota = nota[0]
   			nota.valor = notaJSON['valor']
   		else:
   			disciplina = Disciplina.objects.get(id=notaJSON['disciplina'])
   			nota = Nota(matricula=matricula, disciplina=disciplina, bimestre=notaJSON['bimestre'], tipo=notaJSON['tipo'], valor=notaJSON['valor'])
   		nota.save()	
	return HttpResponse('{"sucess":true}', content_type='application/json') 

@login_required
def boletim(request):
	confs = Configuracoes.objects.get(id=1)
	turmas = Turma.objects.all()
	return render(request, 'boletim.html', {'turmas':turmas, 'ano':confs.ano_letivo})

@login_required
def boletim_turma(request, turma_id):
	confs = Configuracoes.objects.get(id=1)
	ano_letivo = confs.ano_letivo
	matriculas = Matricula.objects.filter(turma_id=turma_id, ano=ano_letivo)
	context = {'matriculas':matriculas}

	return render(request, 'boletim-turma.html', context)

@login_required
def emitir_boletim_turma(request, turma_id): 
	alunos = request.POST.getlist(u'aluno')
	confs = Configuracoes.objects.get(id=1)
	media = confs.media
	ano_letivo =  confs.ano_letivo
	template_boletim = ''
	matriculas = Matricula.objects.filter(turma_id=turma_id, ano=ano_letivo, id__in=map(int, alunos))

	for matricula in matriculas:
		disciplinas = [ x.disciplina for x in matricula.turma.serie.curriculos.all() if x.ativo and not x.disciplina.somente_historico]

		if matricula.turma.serie.modalidade != MODALIDADE_INFANTIL:
			template_boletim = 'template-boletim-aluno-fundamental'
			for dis in disciplinas:
				gerar_boletim_fundamental(dis, matricula.notas.all(), media)
		else:
			template_boletim = 'template-boletim-aluno-infantil'
			for dis in disciplinas:
				gerar_boletim_infantil(dis, matricula.notas.all())
		
		matricula.disciplinas = disciplinas
			
	context =  {'matriculas':matriculas, 'data':datetime.now(), 'ano_letivo':ano_letivo}

	return gerar_PDF(request, context, template_boletim, 'boletim-turma')

@login_required
def rendimento_turma(request, turma_id, disciplina_id, bimestre, tipo_nota):
	confs = Configuracoes.objects.get(id=1)
	media = confs.media
	ano_letivo =  confs.ano_letivo
	form = NotaForm()
	
	matriculas_recuperacao = []
	matriculas = Matricula.objects.filter(turma_id=turma_id, ano=ano_letivo)
	
	for matricula in matriculas:
		notas = matricula.notas.filter(disciplina_id=disciplina_id).filter(bimestre=bimestre)

		matricula.nota = next((n for n in notas if n.tipo == long(tipo_nota)), None)

		if int(tipo_nota) == choices.RECUPERACAO:
			notas_bimestre = [n for n in notas if n.tipo != long(tipo_nota)] 	
			
			if len(notas_bimestre) == 3 and sum([n.valor for n in notas_bimestre])/3 < media:
		   		matriculas_recuperacao.append(matricula)

	matriculas = matriculas_recuperacao if int(tipo_nota) == choices.RECUPERACAO else matriculas 
	matriculas = sorted(matriculas, key=lambda mat: mat.aluno.nome, reverse=False)

	return render(request, 'rendimento-turma.html', {'matriculas':matriculas, 'form':form})

@login_required
def rendimento_turma_recuperacao_final(request, turma_id, disciplina_id):

	confs = Configuracoes.objects.get(id=1)
	media = confs.media
	ano_letivo = confs.ano_letivo
	form = NotaForm()
	matriculas_recuperacao_final = []
	matriculas = Matricula.objects.filter(turma_id=turma_id, ano=ano_letivo)

	for matricula in matriculas:
		medias_bimestrais = []
		notas = matricula.notas.filter(matricula_id=matricula, disciplina_id=disciplina_id)
		counter = Counter([n.bimestre for n in notas])
	
		if len(counter) == 4 and all(notas_cad >= 3 for notas_cad in counter.values()): 
			
			for x, y in choices.BIMESTRE_CHOICES:
				
				nota_recuperacao = [n.valor for n in notas if n.bimestre == x and n.tipo == choices.RECUPERACAO]
				
				if nota_recuperacao:
					medias_bimestrais.append(nota_recuperacao[0])	
				else:
					notas_bimestre = [n.valor for n in notas if n.bimestre == x and n.tipo != choices.RECUPERACAO]
					media_bimestral = sum(notas_bimestre)/3
					medias_bimestrais.append(media_bimestral)

			if sum(medias_bimestrais)/4 < media:
				nota_recuperacao_final = [n for n in notas if n.bimestre == choices.RECUPERACAO_FINAL and n.tipo == choices.RECUPERACAO]
				matricula.nota = nota_recuperacao_final[0] if nota_recuperacao_final else None
				matriculas_recuperacao_final.append(matricula)

	matriculas = sorted(matriculas, key=lambda mat: mat.aluno.nome, reverse=False)

	return render(request, 'rendimento-turma.html', {'matriculas':matriculas_recuperacao_final, 'form':form})


def gerar_boletim_infantil(dis, notas_matricula):
	dis.notas = np.full([4,1], None)

	notas_disciplina = [x for x in notas_matricula if x.disciplina_id == dis.id]
	notas_ordenadas_bimestre = sorted(notas_disciplina, key=lambda x:x.bimestre)
	grupo_notas_bimestre = groupby(notas_ordenadas_bimestre, lambda x: x.bimestre)

	for key, grupo in grupo_notas_bimestre:
		conceito = int([n for n in grupo][0].valor)
		dis.notas[key - 1][0] = dict(choices.NOTA_CONCEITO_CHOICES).get(conceito)


def gerar_boletim_fundamental(dis, notas_matricula, media):

	medias_bimestrais = []
	notas_disciplina = [x for x in notas_matricula if x.disciplina_id == dis.id and x.bimestre != choices.RECUPERACAO_FINAL]
	nota_recuperacao_final = [x for x in notas_matricula if x.disciplina_id == dis.id and x.bimestre == choices.RECUPERACAO_FINAL]
	
	dis.notas = np.full([4,2], None)
	
	notas_ordenadas_bimestre = sorted(notas_disciplina, key=lambda x:x.bimestre)
	grupo_notas_bimestre = groupby(notas_ordenadas_bimestre, lambda x: x.bimestre)
	
	for key, grupo in grupo_notas_bimestre:
		media_bimestral  = None
		
		notas_bimestre   = [n for n in grupo]
		
		nota_recuperacao = [n for n in notas_bimestre if n.tipo == long(choices.RECUPERACAO)]

		# as tres notas sao obigatorias
		if len(notas_bimestre) >= 3:
			media_bimestral = sum([nota.valor for nota in notas_bimestre if nota.tipo != long(choices.RECUPERACAO)])/3
			
		dis.notas[key - 1][0] = media_bimestral
		dis.notas[key - 1][1] = nota_recuperacao[0].valor if nota_recuperacao else None

		medias_bimestrais.append(nota_recuperacao[0].valor if nota_recuperacao else media_bimestral)

	if len(medias_bimestrais) == 4:
		dis.media_final = normal_round(sum(medias_bimestrais)/4)
		dis.recuperacao_final = nota_recuperacao_final[0].valor if nota_recuperacao_final else None
		dis.situacao = 'APR' if dis.media_final >= media or dis.recuperacao_final >= media else 'REP' 







