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
from util.utils import gerar_PDF

from itertools import groupby
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
	return render(request, 'cadastro-notas-recuperacao-final.html', {'ano':confs.ano_letivo,'choices':choices, 'turmas':Turma.objects.all()})

@login_required
def cadastrar_notas(request):

	data = json.loads(json.dumps(request.POST))
	for notaJSON in json.loads(data.get('notas')):
		matricula = Matricula.objects.get(id=notaJSON['matricula'])
		nota = matricula.notas.filter(disciplina_id=notaJSON['disciplina']).filter(bimestre=notaJSON['bimestre']).filter(tipo=notaJSON['tipo'])
   		if nota:
   			nota = nota[0]
   			nota.valor = notaJSON['valor']
   		else:
   			disciplina = Disciplina.objects.get(id=notaJSON['disciplina'])
   			nota = Nota(matricula=matricula, disciplina=disciplina, bimestre=notaJSON['bimestre'], tipo=notaJSON['tipo'], valor=notaJSON['valor'])
   		nota.save()	
	return HttpResponse('{"sucess":true}', content_type='application/json') 


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
		
		# nota = [n for n in notas if n.tipo == long(tipo_nota)]
		
		# matricula.nota = nota[0] if nota else None

		matricula.nota = next((n for n in notas if n.tipo == long(tipo_nota)), None)

		if int(tipo_nota) == choices.RECUPERACAO:
			notas_bimestre = [n for n in notas if n.tipo != long(tipo_nota)] 	
			
			if len(notas_bimestre) == 3 and (sum([n.valor for n in notas_bimestre])/3) < media:
		   		matriculas_recuperacao.append(matricula)

	matriculas = matriculas_recuperacao if int(tipo_nota) == choices.RECUPERACAO else matriculas 

	return render(request, 'rendimento-turma.html', {'matriculas':matriculas, 'form':form})

@login_required
def rendimento_turma_recuperacao_final(request, turma_id, disciplina_id):

	confs = Configuracoes.objects.get(id=1)
	media = confs.media
	ano_letivo =  confs.ano_letivo
	
	form = NotaForm()
	
	matriculas_recuperacao_final = []
	matriculas = Matricula.objects.filter(turma_id=turma_id, ano=ano_letivo)

	for matricula in matriculas:
		medias_bimestrais = []
		notas = matricula.notas.filter(matricula_id=matricula).filter(disciplina_id=disciplina_id)
		
		if len(notas) >= 12: # Todas as notas precisam estar cadastradas, cada tipo
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

	return render(request, 'rendimento-turma.html', {'matriculas':matriculas_recuperacao_final, 'form':form})


@login_required
def boletim_aluno(request, aluno_id):
	confs = Configuracoes.objects.get(id=1)
	media = confs.media
	ano_letivo =  confs.ano_letivo
	template_boletim = ''
	matricula_atual  = Matricula.objects.filter(aluno_id=aluno_id, ano=ano_letivo)
	disciplinas = None
	matricula = None

	if matricula_atual:
		matricula = matricula_atual[0]
		disciplinas = [ x.disciplina for x in matricula.turma.serie.curriculos.all() if x.ativo and not x.disciplina.somente_historico]

		if matricula.turma.serie.modalidade != MODALIDADE_INFANTIL:
			template_boletim = 'boletim-aluno-fundamental'
			for dis in disciplinas:
				gerar_boletim_fundamental(dis, matricula.notas.all(), media)
		else:
			template_boletim = 'boletim-aluno-infantil'
			for dis in disciplinas:
				gerar_boletim_infantil(dis, matricula.notas.all())
			
	context =  {'disciplinas':disciplinas, 'matricula':matricula, 'data':datetime.now()}

	return gerar_PDF(request, context, template_boletim, 'boletim-'+matricula.aluno.nome)


def gerar_boletim_infantil(dis, notas_matricula):
	dis.notas = np.full([4,1], None)

	notas_disciplina = [x for x in notas_matricula if x.disciplina_id == dis.id]
	notas_ordenadas_bimestre = sorted(notas_disciplina, key=lambda x:x.bimestre)
	grupo_notas_bimestre = groupby(notas_ordenadas_bimestre, lambda x: x.bimestre)

	for key, grupo in grupo_notas_bimestre:
		conceito = int([n for n in grupo][0].valor)
		dis.notas[key - 1][0] = dict(choices.NOTA_CONCEITO_CHOICES).get(conceito)
		print dis.notas[key - 1][0]


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
		dis.media_final = sum(medias_bimestrais)/4
		dis.recuperacao_final = nota_recuperacao_final[0].valor if nota_recuperacao_final else None
		dis.situacao = 'APR' if dis.media_final >= media or dis.recuperacao_final >= media else 'REP' 





