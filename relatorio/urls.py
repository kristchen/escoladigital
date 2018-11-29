from django.conf.urls import url
from relatorio import views

urlpatterns = [
    url(r'^relatorio/turma$', views.relatorio_turma, name="relatorio-turma"),
    url(r'^relatorio/situacao-final/disciplina$', views.relatorio_situacao_final_disciplina, name="relatorio-situacao-final-disciplina"),
    url(r'^relatorio/turma/emitir$', views.emitir_relatorio_turma, name="emitir-relatorio-turma"),
    url(r'^relatorio/situacao-final/disciplina/emitir$', views.emitir_relatorio_situacao_final_disciplina, name="emitir-relatorio-situacao-final-disciplina"),
]  