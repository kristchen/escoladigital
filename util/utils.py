from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML, CSS
import datetime
from escola.models import Configuracoes
from random import randint
import math
import decimal



def gerar_PDF(request, context, str_template, filename):

	template = get_template(str_template+'.html')
	
	html = template.render(context)
	
	pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()

	response = HttpResponse(pdf, content_type='application/pdf')
	
	response['Content-Disposition'] = 'inline; filename=%s.pdf' %(filename)

	return response


def gerar_numero_matricula():
	data = datetime.datetime.today()
	ano_letivo =  Configuracoes.objects.get(id=1).ano_letivo 
	ano = str(ano_letivo % 100)
	return ano + str(data.microsecond)


def normal_round(n):
	if n - decimal.Decimal(math.floor(n)) < 0.6:
		return n
	else:
		return round(n)