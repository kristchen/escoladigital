# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import TurmaRelatorioForm, SituacaoFinalDisciplinaRelatorioForm, AtasFinaisForm, ResultadoBimestralForm
from escola.models import Serie, Configuracoes, Turma, Curriculo
from util.utils import gerar_PDF, normal_round
from itertools import chain
from django.contrib.auth.decorators import login_required
from rendimento.choices import RECUPERACAO_FINAL, RECUPERACAO, NOTA_BIMESTRAL, NOTA_PARCIAL, NOTA_EXTRA
from escola.choices import MODALIDADE_FUNDAMENTAL
from itertools import groupby
from collections import Counter
import numpy as np


@login_required
def relatorio_atas_finais(request):
	form = AtasFinaisForm()
	return render(request, 'relatorio-atas-finais.html', {'form':form})


@login_required
def relatorio_situacao_final_disciplina(request):
	form = SituacaoFinalDisciplinaRelatorioForm()
	return render(request, 'relatorio-situacao-final-disciplina.html', {'form':form})

@login_required
def relatorio_turma(request):
	form = TurmaRelatorioForm()
	return render(request, 'relatorio-turma.html', {'form':form})

@login_required
def relatorio_bimestral(request):
	form = ResultadoBimestralForm()
	return render(request, 'relatorio-bimestral.html', {'form':form})

def emitir_relatorio_bimestral(request):
	form = ResultadoBimestralForm(request.POST)
	if form.is_valid():
		dados = form.cleaned_data
		confs = Configuracoes.objects.get(id=1)
		turma = dados['turma']
		disciplina = dados['disciplinas']
		matriculas = turma.alunos.filter(ano=confs.ano_letivo)


		for matricula in matriculas:
			matricula.bimestres = np.full([4], {})
			notas = matricula.notas.filter(disciplina=disciplina.id).order_by('bimestre')
			grupo_notas_bimestre = groupby(notas, lambda x: x.bimestre)
	
			for key, grupo in grupo_notas_bimestre:
				notas_bimestre   = [n for n in grupo]
				bimestre = dict.fromkeys([str('nota_parcial'), str('nota_bimestral'),str('nota_extra')])
				bimestre['nota_parcial']  = next((n for n in notas_bimestre if n.tipo == long(NOTA_PARCIAL)), None)
				bimestre['nota_bimestral']  = next((n for n in notas_bimestre if n.tipo == long(NOTA_BIMESTRAL)), None)
				bimestre['nota_extra'] = next((n for n in notas_bimestre if n.tipo == long(NOTA_EXTRA)), None)
				matricula.bimestres[key - 1] = bimestre

		context = {'matriculas':matriculas, 'confs':confs, 'turma':turma, 'disciplina':disciplina}
		return gerar_PDF(request, context, 'template-relatorio-bimestral', 'relatorio')


	return render(request, 'relatorio-bimestral.html', {'form':form})

def emitir_relatorio_atas_finais(request):
	form = AtasFinaisForm(request.POST)

	if form.is_valid():
		dados = form.cleaned_data
		confs = Configuracoes.objects.get(id=1)
		turma = Turma.objects.get(pk=dados['turma'].id)
		disciplinas = [ x.disciplina for x in turma.serie.curriculos.all() if x.ativo and not x.disciplina.somente_historico]
		matriculas = turma.alunos.filter(ano=confs.ano_letivo)

		for matricula in matriculas:
			
			notas_finais = []
			notas_matricula = matricula.notas.all()
			counter = Counter([n.bimestre for n in notas_matricula])
			
			# se cadastrou todas as notas do bimestre ou o aluno foi transferido
			if len(counter) == 5 or len(counter) == 4 and all(notas_cad >= 3 for notas_cad in counter.values()):
				for dis in disciplinas:
					medias_bimestrais = []
					notas_disciplina = [x for x in notas_matricula if x.disciplina_id == dis.id and x.bimestre != RECUPERACAO_FINAL]
					nota_recuperacao_final = [x for x in notas_matricula if x.disciplina_id == dis.id and x.bimestre == RECUPERACAO_FINAL]
					
					notas_ordenadas_bimestre = sorted(notas_disciplina, key=lambda x:x.bimestre)
					grupo_notas_bimestre = groupby(notas_ordenadas_bimestre, lambda x: x.bimestre)

					for key, grupo in grupo_notas_bimestre:
						media_bimestral  = None
						notas_bimestre   = [n for n in grupo]
						nota_recuperacao = [n for n in notas_bimestre if n.tipo == long(RECUPERACAO)]

						if len(notas_bimestre) >= 3:
							media_bimestral = sum([nota.valor for nota in notas_bimestre if nota.tipo != long(RECUPERACAO)])/3
							medias_bimestrais.append(nota_recuperacao[0].valor if nota_recuperacao and nota_recuperacao[0].valor > media_bimestral else media_bimestral)
					
					if len(medias_bimestrais) == 4:
						media_final = normal_round(sum(medias_bimestrais)/4)
						recuperacao_final = nota_recuperacao_final[0].valor if nota_recuperacao_final else None
						notas_finais.append(recuperacao_final if recuperacao_final and recuperacao_final > media_final else media_final)
					else:
						notas_finais.append(None)
			
				matricula.notas_finais = notas_finais
				matricula.obs = 'Aprovado' if not any(nota for nota in notas_finais if nota < 6) else 'Reprovado'

		context = {'disciplinas':disciplinas, 'matriculas':matriculas, 'confs':confs, 'turma':turma}
		
		return gerar_PDF(request, context, 'template-relatorio-atas-finais', 'relatorio')

	return render(request, 'relatorio-atas-finais.html', {'form':form})


def emitir_relatorio_situacao_final_disciplina(request):
	form = SituacaoFinalDisciplinaRelatorioForm(request.POST)
	
	if form.is_valid():
	
		dados  = form.cleaned_data
		confs  = Configuracoes.objects.get(id=1)
		disciplina = dados['disciplina']
		curriculos = Curriculo.objects.filter(disciplina_id=disciplina.id)
		
		turmas = []
		for curr in curriculos:
			turmas += [turma for turma in curr.serie.turmas.all()]
		
		turmas_relatorio = []

		for turma in turmas:
			
			if turma.serie.modalidade == MODALIDADE_FUNDAMENTAL:

				alunos_relatorio = []
				
				for matricula in turma.alunos.filter(ano=confs.ano_letivo):
					
					notas_disciplina = matricula.notas.filter(disciplina_id=disciplina.id)
					counter = Counter([n.bimestre for n in notas_disciplina if n.bimestre != RECUPERACAO_FINAL])

					if len(counter) == 4 and all(notas_cad >= 3 for notas_cad in counter.values()): 

						# caso o aluno tenha feito a recuperacao final
						# nota_final = [nf.valor for nf in notas_disciplina if nf.bimestre == RECUPERACAO_FINAL]

						medias_bimestrais = []
						notas_ordenadas_bimestre = sorted(notas_disciplina, key=lambda x:x.bimestre)
						grupo_notas_bimestre = groupby(notas_ordenadas_bimestre, lambda x: x.bimestre)

						for key, grupo in grupo_notas_bimestre:
							notas_bimestre   = [n for n in grupo]
							
							nota_recuperacao = next((n for n in notas_bimestre if n.tipo == long(RECUPERACAO)), None)
							
							media_bimestral = sum([nota.valor for nota in notas_bimestre if nota.tipo != long(RECUPERACAO)])/3

							medias_bimestrais.append(nota_recuperacao.valor if nota_recuperacao and nota_recuperacao.valor > media_bimestral else media_bimestral)	
							nota_final = normal_round(sum(medias_bimestrais)/4)
						
						if nota_final < confs.media:
							matricula.nota_final = nota_final
							alunos_relatorio.append(matricula)
				
				turma.alunos_relatorio = alunos_relatorio
				turmas_relatorio.append(turma)

		context = {'turmas':turmas_relatorio, 'disciplina': disciplina, 'conf':confs}

		return gerar_PDF(request, context, 'template-relatorio-situacao-final-disciplina', 'relatorio')

	return render(request, 'relatorio-turma.html', {'form':form})

def emitir_relatorio_turma(request):
	form = TurmaRelatorioForm(request.POST)
	if form.is_valid():
		dados  = form.cleaned_data
		confs  = Configuracoes.objects.get(id=1)

		if not dados['sequencia']:
			turmas = Turma.objects.filter(serie_id=dados['serie'].id)
		else:
			turmas = Turma.objects.filter(serie_id=dados['serie'].id).filter(sequencia=dados['sequencia'])

		matriculas = [turma.alunos.filter(ano=confs.ano_letivo) for turma in turmas]
		matriculas = list(chain.from_iterable(matriculas))
		matriculas.sort(key=lambda mat : mat.aluno.nome, reverse=False)
		context = {'matriculas':matriculas, 'turma':next(iter(turmas),None), 'sequencia':dados['sequencia'], 'conf':confs}
		
		return gerar_PDF(request, context, 'template-relatorio-turma', 'relatorio')

	return render(request, 'relatorio-turma.html', {'form':form})