from django.conf.urls import url
from escola import views

urlpatterns = [
    url(r'^escola/serie/cadastro$', views.cadastro_serie, name="cadastro-serie"),
    url(r'^escola/serie/(?P<serie_id>\d+)/disciplinas$', views.lista_disciplinas_serie),
    url(r'^escola/serie/(?P<serie_id>\d+)/disciplinas/historico$', views.lista_disciplinas_serie_historico),
    url(r'^escola/serie/(?P<serie_id>\d+)/disciplinas/rendimento$', views.lista_disciplinas_serie_rendimento),
    url(r'^escola/serie/disciplinas/associar$', views.associar_disciplina, name="associar-disciplina"),
    url(r'^escola/disciplina/cadastro$', views.cadastro_disciplina, name="cadastro-disciplina"),
    url(r'^escola/disciplina/cadastrar$', views.cadastrar_disciplina, name="cadastrar-disciplina"),
    url(r'^escola/disciplina/(?P<disciplina_id>\d+)/status/alterar$', views.alterar_status_disciplina),
    url(r'^escola/disciplina/(?P<disciplina_id>\d+)/edicao$', views.edicao_disciplina, name='edicao-disciplina'),
    url(r'^escola/disciplina/(?P<disciplina_id>\d+)/editar$', views.editar_disciplina, name='editar-disciplina'),
    url(r'^escola/turma/(?P<turma_id>\d+)/status/alterar$', views.alterar_status_turma),
    url(r'^escola/turma/cadastro$', views.cadastro_turma, name="cadastro-turma"),
    url(r'^escola/turma/cadastrar$', views.cadastrar_turma, name="cadastrar-turma"),
    url(r'^escola/configuracoes/edicao$', views.edicao_configuracoes, name="edicao-configuracoes"),
    url(r'^escola/configuracoes/editar$', views.editar_configuracoes, name="editar-configuracoes"),

]  



