# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import TurmaRelatorioForm
from escola.models import Serie, Configuracoes, Turma
from util.utils import gerar_PDF
from itertools import chain

def relatorio_turma(request):
	form = TurmaRelatorioForm()
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