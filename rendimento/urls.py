from django.conf.urls import url
from rendimento import views

urlpatterns = [
    url(r'^rendimento/notas/cadastro$',  views.cadastro_notas,  name="cadastro-notas"),
    url(r'^rendimento/notas/cadastrar$', views.cadastrar_notas, name="cadastrar-notas"),
    url(r'^rendimento/turma/(?P<turma_id>\d+)/disciplina/(?P<disciplina_id>\d+)/bimestre/(?P<bimestre>\d+)/tipo/(?P<tipo_nota>\d+)$', views.rendimento_turma),
    url(r'^rendimento/notas/recuperacao/cadastro$',  views.cadastro_notas_recuperacao_final,  name="cadastro-notas-recuperacao-final"),
    url(r'^rendimento/turma/recuperacao/(?P<turma_id>\d+)/disciplina/(?P<disciplina_id>\d+)$', views.rendimento_turma_recuperacao_final),
    url(r'^rendimento/aluno/(?P<aluno_id>\d+)/boletim$', views.boletim_aluno, name='boletim-aluno'),


]  

