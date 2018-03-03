from django.conf.urls import url
from aluno import views

urlpatterns = [
    url(r'^aluno/cadastro$', views.cadastro_aluno, name="cadastro-aluno"),
    url(r'^aluno/cadastrar$', views.cadastrar_aluno, name="cadastrar-aluno"),
    url(r'^aluno/pesquisa$', views.pesquisa_aluno, name="pesquisa-aluno"),
    url(r'^aluno/pesquisar$', views.pesquisar_aluno, name="pesquisar-aluno"),
    url(r'^aluno/(?P<aluno_id>\d+)/detalhe$', views.detalhe_aluno, name="detalhe-aluno"),
    url(r'^aluno/(?P<aluno_id>\d+)/edicao$', views.edicao_aluno, name="edicao-aluno"),
    url(r'^aluno/(?P<aluno_id>\d+)/editar$', views.editar_aluno, name="editar-aluno"),
    url(r'^aluno/(?P<aluno_id>\d+)/matricula$', views.matricula_aluno, name="matricula-aluno"),
    url(r'^aluno/(?P<aluno_id>\d+)/matricular$', views.matricular_aluno, name="matricular-aluno"),
	url(r'^aluno/(?P<aluno_id>\d+)/declaracao$', views.declaracao_aluno, name="declaracao-aluno"),
    url(r'^aluno/(?P<aluno_id>\d+)/declaracao/emitir$', views.emitir_declaracao_aluno, name="emitir-declaracao-aluno")

]  