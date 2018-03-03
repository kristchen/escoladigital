from django.conf.urls import url
from historico import views

urlpatterns = [
    url(r'^historico/(?P<aluno_id>\d+)/cadastro$', views.cadastro_historico, name="cadastro-historico"),
  	url(r'^historico/(?P<aluno_id>\d+)/cadastrar$', views.cadastrar_historico),
  	url(r'^historico/(?P<aluno_id>\d+)/detalhe$', views.detalhe_historico, name='detalhe-historico'),
  	url(r'^historico/(?P<aluno_id>\d+)/emitir$', views.emitir_historico, name='emitir-historico'),
  	url(r'^historico/(?P<historico_id>\d+)/edicao$', views.edicao_historico, name='edicao-historico'),
  	url(r'^historico/editar$', views.editar_historico, name='editar-historico'),
  	url(r'^historico/instituicoes$', views.lista_instituicoes_historico)

]  



