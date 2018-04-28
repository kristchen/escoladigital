from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML, CSS
import datetime
from random import randint


def gerar_PDF(request, context, str_template, filename):

	template = get_template(str_template+'.html')
	
	html = template.render(context)
	
	pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()

	response = HttpResponse(pdf, content_type='application/pdf')
	
	response['Content-Disposition'] = 'inline; filename=%s.pdf' %(filename)

	return response


def gerar_numero_matricula():
	ano = str(datetime.date.today().year % 100)
	return ano + str(randint(10000, 99999))