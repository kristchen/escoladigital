# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from models import Aluno, Endereco, Matricula

admin.site.register(Aluno, SimpleHistoryAdmin)
admin.site.register(Endereco, SimpleHistoryAdmin)
admin.site.register(Matricula, SimpleHistoryAdmin)