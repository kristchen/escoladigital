# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

APROVADO  = True
REPROVADO = False

SITUACAO_CHOICES = (
	(APROVADO,  'Aprovado'),
	(REPROVADO, 'Reprovado')
)

ANO_HISTORICO_CHOICES = tuple((n, str(n)) for n in range(1995, datetime.now().year + 1))


UF_CHOICES = (
('AC','AC'),
('AL','AL'),
('AM','AM'),
('AP','AP'),
('BA','BA'),
('CE','CE'),
('DF','DF'),
('ES','ES'),
('GO','GO'),
('MA','MA'),
('MG','MG'),
('MS','MS'),
('MT','MT'),
('PA','PA'),
('PB','PB'),
('PE','PE'),
('PI','PI'),
('PR','PR'),
('RJ','RJ'),
('RN','RN'),
('RO','RO'),
('RR','RR'),
('RS','RS'),
('SC','SC'),
('SE','SE'),
('SP','SP'),
('TO','TO')
)