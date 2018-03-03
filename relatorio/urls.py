from django.conf.urls import url
from relatorio import views

urlpatterns = [
    url(r'^relatorio/turma$', views.relatorio_turma, name="relatorio-turma"),
    url(r'^relatorio/turma/emitir$', views.emitir_relatorio_turma, name="emitir-relatorio-turma"),
]  