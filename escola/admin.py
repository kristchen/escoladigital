# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from models import Serie, Configuracoes, Curriculo, Turma

admin.site.register(Serie, SimpleHistoryAdmin)
admin.site.register(Configuracoes, SimpleHistoryAdmin)
admin.site.register(Curriculo, SimpleHistoryAdmin)
admin.site.register(Turma, SimpleHistoryAdmin)
