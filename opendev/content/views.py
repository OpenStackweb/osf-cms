from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from menus.models import BigHeaderMenu
from content.models import Page


def about(request):
	template = loader.get_template('base.html')
	page = Page.objects.get(title='About')
	header_menus = BigHeaderMenu.objects.all().order_by('order')
	context = {
		'pages': header_menus,
		'title': page.title,
		'page' : page,
	}
	return HttpResponse(template.render(context, request))


def sponsors(request):
	return HttpResponse('Sponsors work')

def schedule(request):
	return HttpResponse('Schedule work')

def videos(request):
	return HttpResponse('Videos work')

def faq (request):
	return HttpResponse('FAQ work')
