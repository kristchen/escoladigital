# -*- coding: utf-8 -*-
NOTA_PARCIAL = 1
NOTA_BIMESTRAL = 2
RECUPERACAO = 3
NOTA_EXTRA = 4

TIPO_NOTA_CHOICES = (
	(NOTA_PARCIAL, 'Nota Parcial'),
	(NOTA_BIMESTRAL, 'Nota Bimestral'),
	(NOTA_EXTRA, 'Nota Extra'),
	(RECUPERACAO, 'Recuperação')
)

BIMESTRE_CHOICES = (
	(1, '1° Bimestre'),
	(2, '2° Bimestre'),
	(3, '3° Bimestre'),
	(4, '4° Bimestre')	
)

RECUPERACAO_FINAL = 5

NOTA_CONCEITO_CHOICES = (
	(4, 'Precisa Melhorar'),
	(6, 'Regular'),
	(8, 'Bom'),
	(10,'Excelente')
)