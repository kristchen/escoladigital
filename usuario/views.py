# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pygal
from pygal.style import DefaultStyle
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from aluno.models import Matricula
from escola.models import Configuracoes, Serie
from escola import choices
from itertools import groupby
from django.db.models import Count

@login_required
def home(request):
    confs = Configuracoes.objects.get(id=1)
    matriculas = Matricula.objects.filter(ano=confs.ano_letivo)
    
    total = len(matriculas)
    
    fundamental = len([matricula for matricula in matriculas if matricula.turma.serie.modalidade == choices.MODALIDADE_FUNDAMENTAL])
    infantil = len([matricula for matricula in matriculas if matricula.turma.serie.modalidade == choices.MODALIDADE_INFANTIL])
    chart_modalidade = gerar_grafico_pie('Alunos por modalidade',[('Infantil', infantil), ('Fundamental', fundamental)])
    
    manha = len([matricula for matricula in matriculas if matricula.turma.sequencia == 'A'])
    tarde = len([matricula for matricula in matriculas if matricula.turma.sequencia == 'B'])
    chart_turno = gerar_grafico_pie('Alunos por turno',[('Manhã', manha), ('Tarde', tarde)])
    
    agrupadas = Serie.objects.filter(turmas__alunos__ano=confs.ano_letivo).annotate(num_al=Count('turmas__alunos')).order_by('id')
    lista_serie = [serie.descricao for serie in agrupadas]
    lista_alunos = [serie.num_al for serie in agrupadas]
    chart_series = gerar_grafico_barra('Alunos por série', lista_alunos, lista_serie)

    context = {'chart_series':chart_series,'chart_modalidade':chart_modalidade, 'chart_turno':chart_turno, 'total':total, 'confs':confs}
    return render(request, 'home.html', context )


def gerar_grafico_pie(titulo, lista ):
    pie = pygal.Pie(dynamic_print_values=False, print_values=True, height=400, width=400, legend_at_bottom=True, style=DefaultStyle(
                    value_font_family='googlefont:Raleway',
                    value_font_size=30,
                    value_colors=('white',)))
    pie.title = titulo
    for value in lista:
        pie.add(value[0], value[1])
        
    return pie.render_data_uri() 
    

def gerar_grafico_barra(titulo, lista_alunos, lista_serie):
    line_chart = pygal.Bar(dynamic_print_values=False, print_values=True, height=200, width=700, show_y_labels=False, x_label_rotation=20, rounded_bars=5, style=DefaultStyle(
                            value_font_family='googlefont:Raleway',
                            value_font_size=20,
                            value_colors=('white',)))
    line_chart.title = titulo
    line_chart.x_labels = lista_serie
    line_chart.add(None, lista_alunos)
    line_chart.render()
        
    return line_chart.render_data_uri() 

