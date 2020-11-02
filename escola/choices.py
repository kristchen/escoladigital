# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

TURMA_SEQUENCIA_CHOICES = (
		('A','A'),
		('B','B')
)

MODALIDADE_INFANTIL = 'I'
MODALIDADE_FUNDAMENTAL = 'F'
MODALIDADE_MEDIO = 'M'

MODALIDADE_ENSINO_CHOICES = (
	(MODALIDADE_INFANTIL, 'Educação Infantil'),
	(MODALIDADE_FUNDAMENTAL, 'Ensino Fundamental'),
	(MODALIDADE_MEDIO, 'Ensino Médio')
)

SERIES_CHOICES = (
	('Infantil I', 'Infantil I' ),
	('Infantil II', 'Infantil II'),
	('Infantil III', 'Infantil III'),
	('Infantil IV', 'Infantil IV'),
	('Infantil V', 'Infantil V'),
	('1° Ano', '1° Ano'),
	('2° Ano', '2° Ano'),
	('3° Ano', '3° Ano'),
	('4° Ano', '4° Ano'),
	('5° Ano', '5° Ano'),
	('6° Ano', '6° Ano'),
	('7° Ano', '7° Ano'),
	('8° Ano', '8° Ano'),
	('9° Ano', '9° Ano'),
)

ANO_LETIVO_CHOICES = tuple((n, str(n)) for n in range(1995, datetime.now().year + 1))

BIMESTRE_CHOICES = (
	(1, '1° Bimestre'),
	(2, '2° Bimestre'),
	(3, '3° Bimestre'),
	(4, '4° Bimestre')	
)